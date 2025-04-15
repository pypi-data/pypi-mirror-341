import numpy as np
import torch
from torch import nn
from torch import optim
from pathlib import Path
from typing import Union, List, Tuple, Collection, Optional, Set, Callable
from sklearn.model_selection import train_test_split
from torch.nn import functional as F
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import DataLoader, Dataset, TensorDataset
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    classification_report
)

from model_wrapper import log_utils
from model_wrapper.utils import convert_to_tensor, convert_data, acc_predict, get_device, \
    get_dataset_collate_fn, get_dataset2_collate_fn
from model_wrapper.training import (
    evaluate,
    Trainer,
    EvalTrainer,
    acc_evaluate,
    ClassTrainer,
    EvalClassTrainer,
    r2_evaluate,
    RegressTrainer,
    EvalRegressTrainer,
)

__all__ = [
    "ModelWrapper",
    "SimpleModelWrapper",
    "ClassifyModelWrapper",
    "SimpleClassifyModelWrapper",
    "SplitClassifyModelWrapper",
    "RegressModelWrapper",
    "SimpleRegressModelWrapper",
    "SplitRegressModelWrapper",
]


class ModelWrapper:
    """
    Examples
    --------
    >>> model_wrapper = ModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.logits(X_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        self.device = get_device(device)
        if isinstance(model_or_path, nn.Module):
            model_or_path = model_or_path.to(self.device)
            self.model, self.best_model = model_or_path, model_or_path
        elif isinstance(model_or_path, (str, Path)):
            self.model = torch.load(model_or_path, map_location=self.device, weights_only=False)
            self.best_model = self.model

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_set:
            trainer = EvalTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, show_progress, eps
            )
        else:
            trainer = Trainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, eps
            )
        return histories

    def logits(self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128) -> torch.Tensor:
        self.best_model.eval()
        # 多个 X 值，用tuple、set或list封装, 如果是list, 其元素是torch.Tensor或numpy.ndarray
        if is_multi_value(X):
            size = len(X[0])
            X = tuple((x if torch.is_tensor(x) else convert_to_tensor(x)).to(self.device) for x in X)
            if size >= (batch_size << 1):
                chunks = size // batch_size if size % batch_size == 0 else size // batch_size + 1
                X = [torch.chunk(x, chunks, dim=0) for x in X]
                with torch.inference_mode():
                    preds = [self.best_model(*x) for x in zip(*X)]
                return torch.cat(preds, dim=0)
            
            with torch.inference_mode():
                return self.best_model(*X)

        # 只有一个 X 值
        size = len(X)
        if isinstance(X, (List, np.ndarray)):
            X = convert_to_tensor(X, 2).to(self.device)
        
        if size >= (batch_size << 1):
            chunks = size // batch_size if size % batch_size == 0 else size // batch_size + 1
            with torch.inference_mode():
                preds = [self.best_model(x) for x in torch.chunk(X, chunks, dim=0)]
            return torch.cat(preds, dim=0)

        with torch.inference_mode():
            return self.best_model(X.to(self.device))

    def evaluate(
        self, val_set: Dataset, batch_size=128, num_workers: int = 0, collate_fn: Callable = None
    ) -> float:
        """
        This method is used to evaluate the model's performance on a validation dataset.
        It returns the loss value as a metric of performance.

        Parameters:
        - val_set: Dataset, the validation dataset, which is an instance of the Dataset class.
        - batch_size: int, default 128, the number of samples per batch during evaluation.
        - num_workers: int, default 0, the number of subprocesses to use for data loading.
        - collate_fn: function, default None, a function to merge samples into a batch.

        Returns:
        - float: The loss value representing the model's performance on the validation dataset.
        """
        # Initialize the DataLoader for the validation dataset
        val_loader = DataLoader(
            dataset=val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        # Call the evaluate function to calculate and return the loss
        return evaluate(self.best_model, val_loader, self.device)

    def save(
        self,
        best_model_path: Union[str, Path] = "./best_model.pt",
        last_model_path: Union[str, Path] = "./last_model.pt",
        mode: str = "both",
    ):
        """
        Saves the model based on the specified mode.

        This function saves the model to the specified path(s) according to the `mode` parameter.
        It supports saving either the best model, the last model, or both, providing flexibility
        in model management during training or evaluation processes.

        :param best_model_path: The file path for saving the best model. Defaults to "./best_model.pt".
        :param last_model_path: The file path for saving the last model. Defaults to "./last_model.pt".
        :param mode: The mode for saving the model. Can be "both", "best", or "last". Defaults to "both".
        :return: None
        """
        # Ensure the mode parameter is valid
        assert mode in ("both", "best", "last")

        # Save the model(s) according to the specified mode
        if mode == "both":
            torch.save(self.model, last_model_path)
            torch.save(self.best_model, best_model_path)
        elif mode == "best":
            torch.save(self.best_model, best_model_path)
        elif mode == "last":
            torch.save(self.model, last_model_path)

    def save_state_dict(
        self,
        best_model_path: Union[str, Path] = "./best_model.pth",
        last_model_path: Union[str, Path] = "./last_model.pth",
        mode: str = "both",
    ):
        """
        Saves the model based on the specified mode.

        This function saves the model to the specified path(s) according to the `mode` parameter.
        It supports saving either the best model, the last model, or both, providing flexibility
        in model management during training or evaluation processes.

        :param best_model_path: The file path for saving the best model. Defaults to "./best_model.pth".
        :param last_model_path: The file path for saving the last model. Defaults to "./last_model.pth".
        :param mode: The mode for saving the model. Can be "both", "best", or "last". Defaults to "both".
        :return: None
        """
        # Ensure the mode parameter is valid
        assert mode in ("both", "best", "last")

        # Save the model(s) according to the specified mode
        if mode == "both":
            torch.save(self.model.state_dict(), last_model_path)
            torch.save(self.best_model.state_dict(), best_model_path)
        elif mode == "best":
            torch.save(self.best_model.state_dict(), best_model_path)
        elif mode == "last":
            torch.save(self.model.state_dict(), last_model_path)

    def load(self, model_path: Union[str, Path] = "./best_model.pt"):
        self.model = torch.load(model_path, map_location=self.device)
        self.best_model = self.model

    def load_state_dict(self, model_path: Union[str, Path] = "./best_model.pth"):
        state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state_dict)
        self.best_model.load_state_dict(state_dict)


class SimpleModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SimpleModelWrapper(model)
    >>> model_wrapper.train(X, y, collate_fn)
    >>> model_wrapper.logits(X_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List], Union[torch.Tensor, np.ndarray, List]
        ] = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
    ) -> dict:
        if val_data:
            train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        else:
            val_set = None
            train_set, collate_fn = get_dataset_collate_fn(X, y)

        return super().train(train_set, val_set, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                                batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory,
                                pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                                drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps=eps)
    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
    ) -> float:
        """return loss"""
        X, y = convert_data(X, y)
        val_set = TensorDataset(X, y)
        return super().evaluate(val_set, batch_size, num_workers, collate_fn)


class ClassifyModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = ClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)
        self.classes = classes

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if val_set:
            trainer = EvalClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, show_progress, eps, monitor
            )
        else:
            trainer = ClassTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, eps, monitor
            )
        return histories

    def predict(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: int = 0.5
    ) -> np.ndarray:
        """
        :param X:
        :param batch_size:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(X, batch_size)
        return acc_predict(logits, threshold)

    def predict_classes(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: int = 0.5
    ) -> list:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        pred = self.predict(X, batch_size, threshold)
        return self._predict_classes(pred.ravel())

    def _predict_classes(self, pred: np.ndarray) -> np.ndarray:
        if self.classes:
            return [self.classes[i] for i in pred]
        else:
            log_utils.warn("Warning: classes not be specified")
            return pred

    def predict_proba(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: int = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        logits = self.logits(X, batch_size)
        return self._proba(logits, threshold)

    @staticmethod
    def _proba(
        logits: torch.Tensor, threshold: int = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        :param logits:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        shape = logits.shape
        shape_len = len(shape)
        if (shape_len == 2 and shape[1] > 1) or shape_len > 2:
            # 多分类
            result = F.softmax(logits, dim=-1).max(-1)
            return result.indices.numpy(), result.values.numpy()
        else:
            # 二分类
            logits = logits.numpy()
            if shape_len == 2:
                logits = logits.ravel()
            return (np.where(logits >= threshold, 1, 0).astype(np.int64), 
                    np.where(logits >= 0.5, logits, 1 - logits))

    def predict_classes_proba(
        self, X: Union[torch.Tensor, np.ndarray, List, Tuple], batch_size=128, threshold: int = 0.5
    ) -> Tuple[list, np.ndarray]:
        """
        :param X:
        :param threshold: 二分类且模型输出为一维概率时生效
        """
        indices, values = self.predict_proba(X, batch_size, threshold)
        return self._predict_classes(indices.ravel()), values

    def evaluate(
        self,
        val_set: Dataset,
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: int = 0.5,
    ) -> float:
        """
        :param val_set:
        :param threshold: 二分类且模型输出为一维概率时生效
        :return accuracy
        """
        val_loader = DataLoader(
            dataset=val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        _, acc = acc_evaluate(self.best_model, val_loader, self.device, threshold)
        return acc
    
    def classification_report(
        self, 
        data_set: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: int = 0.5,
        target_names: List[str] = None
    ) -> Union[str, dict]:
        data_loader = DataLoader(
            dataset=data_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        self.best_model.eval()
        logit_list = []
        label_list = []
        with torch.no_grad():
            for x, y in data_loader:
                logit_list.append(self.best_model(x))
                label_list.append(y)
        logits = torch.cat(logit_list, dim=0)
        labels = torch.cat(label_list, dim=0)
        pred = acc_predict(logits, threshold)
        return classification_report(labels.numpy(), pred, target_names=target_names or self.classes)


class SimpleClassifyModelWrapper(ClassifyModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SimpleClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y val_data, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List],
            Union[torch.LongTensor, np.ndarray, List],
        ] = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if val_data:
            train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        else:
            val_set = None
            train_set, collate_fn = get_dataset_collate_fn(X, y)
        
        return super().train(train_set, val_set, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                                 batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory,
                                 pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                                 drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor)

    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
        threshold: int = 0.5,
    ):
        """return accuracy"""
        X, y = convert_data(X, y)
        data_set = TensorDataset(X, y)
        return super().evaluate(
            data_set, batch_size, num_workers, collate_fn, threshold
        )

    def classification_report(
            self, 
            X: Union[torch.Tensor, np.ndarray, List, Tuple], 
            y: Union[torch.LongTensor, np.ndarray, List], 
            batch_size=128,
            threshold: int = 0.5,
            target_names: Optional[List] = None,
    ) -> Union[str, dict]:
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()

        pred = self.predict(X, batch_size, threshold)
        return classification_report(y, pred, target_names=target_names or self.classes)
        

class SplitClassifyModelWrapper(SimpleClassifyModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SplitClassifyModelWrapper(model, classes=classes)
    >>> model_wrapper.train(X, y val_data, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        classes: Collection[str] = None,
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, classes, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor: str = "accuracy"
    ) -> dict:
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = split_fn(X, y, test_size=val_size, random_state=random_state)
            val_data = (X_test, y_test)
        else:
            val_data = None
            X_train, y_train = X, y

        return super().train(X_train, y_train, val_data, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                            batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory,
                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor)
        

class RegressModelWrapper(ModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = RegressModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        train_set: Dataset,
        val_set: Dataset = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score"
    ) -> dict:
        if val_set:
            trainer = EvalRegressTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                eval_batch_size,
                num_workers,
                num_eval_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, val_set, collate_fn, show_progress, eps, monitor
            )
        else:
            trainer = RegressTrainer(
                epochs,
                optimizer,
                scheduler,
                lr,
                T_max,
                batch_size,
                num_workers,
                pin_memory,
                pin_memory_device,
                persistent_workers,
                early_stopping_rounds,  # 早停，等10轮决策，评价指标不在变化，停止
                print_per_rounds,
                drop_last,
                checkpoint_per_rounds,
                checkpoint_name,
                self.device,
            )
            self.best_model, histories = trainer.train(
                self.model, train_set, collate_fn, show_progress, eps, monitor
            )
        return histories

    def predict(self, X: Union[torch.Tensor, np.ndarray, List[float], Tuple], batch_size=128) -> np.ndarray:
        return self.logits(X, batch_size).cpu().numpy()

    def mae(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> float:
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()

        pred = self.predict(X, batch_size)
        return mean_absolute_error(y.ravel(), pred.ravel())

    def mse(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> float:
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()

        pred = self.predict(X, batch_size)
        return mean_squared_error(y.ravel(), pred.ravel())

    def rmse(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> float:
        return np.sqrt(self.mse(X, y, batch_size))

    def evaluate(
        self, val_set: Dataset, batch_size=128, num_workers: int = 0, collate_fn: Callable = None
    ) -> float:
        """return r2_score"""
        val_loader = DataLoader(
            dataset=val_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        _, r2 = r2_evaluate(self.best_model, val_loader, self.device)
        return r2
    
    def metrics(
        self, 
        data_set: Dataset, 
        batch_size=128,
        num_workers: int = 0,
        collate_fn: Callable = None,
    ) -> Union[str, dict]:
        data_loader = DataLoader(
            dataset=data_set,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
        self.best_model.eval()
        pred_list = []
        target_list = []
        with torch.no_grad():
            for x, y in data_loader:
                pred_list.append(self.best_model(x))
                target_list.append(y)
        preds = torch.cat(pred_list, dim=0).ravel()
        targets = torch.cat(target_list, dim=0).ravel()
        mse = mean_squared_error(targets, preds)
        return {
            "MAE": mean_absolute_error(targets, preds),
            "MSE": mse,
            "RMSE": np.sqrt(mse),
            "R2": r2_score(targets, preds),
        }


class SimpleRegressModelWrapper(RegressModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SimpleRegressModelWrapper(model)
    >>> model_wrapper.train(train_set, val_set, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(test_set, collate_fn=collate_fn)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.Tensor, np.ndarray, List],
        val_data: Tuple[
            Union[torch.Tensor, np.ndarray, List], Union[torch.Tensor, np.ndarray, List]
        ] = None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score"
    ) -> dict:
        if val_data:
            train_set, val_set, collate_fn = get_dataset2_collate_fn(X, y, val_data)
        else:
            val_set = None
            train_set, collate_fn = get_dataset_collate_fn(X, y)
            
        return super().train(train_set, val_set, collate_fn, epochs, optimizer, scheduler, lr, T_max,
                            batch_size, eval_batch_size, num_workers, num_eval_workers, pin_memory,
                            pin_memory_device, persistent_workers, early_stopping_rounds, print_per_rounds, 
                            drop_last, checkpoint_per_rounds, checkpoint_name, show_progress, eps, monitor)

    def evaluate(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        batch_size=128,
    ) -> float:
        """return loss"""
        if isinstance(y, list):
            y = np.array(y)
        elif torch.is_tensor(y):
            y = y.numpy()
        pred = self.predict(X, batch_size)
        return r2_score(y.ravel(), pred.ravel())
    
    def metrics(
        self,
        X: Union[torch.Tensor, np.ndarray, List[float]],
        y: Union[torch.Tensor, np.ndarray, List[float]],
        batch_size=128
    ) -> dict:
        if isinstance(y, list):
            y = np.array(y).ravel()
        elif torch.is_tensor(y):
            y = y.numpy().ravel()
        pred = self.predict(X, batch_size).ravel()
        mse = mean_squared_error(y, pred)
        return {
            "MAE": mean_absolute_error(y, pred),
            "MSE": mse,
            "RMSE": np.sqrt(mse),
            "R2": r2_score(y, pred),
        }


class SplitRegressModelWrapper(SimpleRegressModelWrapper):
    """
    Examples
    --------
    >>> model_wrapper = SplitRegressModelWrapper(model)
    >>> model_wrapper.train(X, y, collate_fn)
    >>> model_wrapper.predict(X_test)
    >>> model_wrapper.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        model_or_path: Union[nn.Module, str, Path],
        device: Union[str, int, torch.device] = "auto",
    ):
        super().__init__(model_or_path, device)

    def train(
        self,
        X: Union[torch.Tensor, np.ndarray, List, Tuple],
        y: Union[torch.LongTensor, np.ndarray, List],
        val_size=0.2,
        random_state=None,
        collate_fn: Callable = None,
        epochs: int = 100,
        optimizer: Union[type, optim.Optimizer] = None,
        scheduler: LRScheduler = None,
        lr: float = 0.001,
        T_max: int = 0,
        batch_size: int = 64,
        eval_batch_size: int = 128,
        num_workers: int = 0,
        num_eval_workers: int = 0,
        pin_memory: bool = False,
        pin_memory_device: str = "",
        persistent_workers: bool = False,
        early_stopping_rounds: int = None,
        print_per_rounds: int = 1,
        drop_last: bool = False,
        checkpoint_per_rounds: int = 0,
        checkpoint_name="model.pt",
        show_progress=True,
        eps=1e-5,
        monitor="r2_score"
    ) -> dict:
        if 0.0 < val_size < 1.0:
            X_train, X_test, y_train, y_test = split_fn(X, y, test_size=val_size, random_state=random_state)
            val_data = (X_test, y_test)
        else:
            val_data = None
            X_train, y_train = X, y

        return super().train(
            X_train,
            y_train,
            val_data,
            collate_fn,
            epochs,
            optimizer,
            scheduler,
            lr,
            T_max,
            batch_size,
            eval_batch_size,
            num_workers,
            num_eval_workers,
            pin_memory,
            pin_memory_device,
            persistent_workers,
            early_stopping_rounds,
            print_per_rounds,
            drop_last,
            checkpoint_per_rounds,
            checkpoint_name,
            show_progress,
            eps,
            monitor
        )
        

def split_fn(
    X: Union[torch.Tensor, np.ndarray, List, Tuple],
    y: Union[torch.LongTensor, np.ndarray, List],
    test_size: float,
    random_state: int,
) -> Tuple[Union[torch.Tensor, np.ndarray, List, Tuple], Union[torch.LongTensor, np.ndarray, List]]:
    # 多个 X 值，用tuple、set或list封装, 如果是list, 其元素是torch.Tensor或numpy.ndarray
    if is_multi_value(X):
        X = tuple((x if torch.is_tensor(x) else convert_to_tensor(x)) for x in X)
        split_data = train_test_split(*X, y, test_size=test_size, random_state=random_state)
        
        X = split_data[:-2]
        X_train, X_test = X[::2], X[1::2]

        y_train, y_test = split_data[-2:]
        return tuple(X_train), tuple(X_test), y_train, y_test
    else:
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
def is_multi_value(X: Union[torch.Tensor, np.ndarray, List, Tuple]):
    # 用tuple、set或list封装, 如果是list, 其元素是torch.Tensor或numpy.ndarray
    return isinstance(X, (Tuple, Set)) \
        or (isinstance(X, List) and (isinstance(X[0], (torch.Tensor, np.ndarray)) or len(X) < 8))
    