import torch
import torch.nn as nn
from torch.nn import LSTM


class LSTMModel(nn.Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Extract model parameters from kwargs
        self.input_size = kwargs.get("input_size", 1)
        self.hidden_size = kwargs.get("hidden_size", 64)
        self.num_layers = kwargs.get("num_layers", 2)
        self.output_size = kwargs.get("output_size", 1)
        self.dropout = kwargs.get("dropout", 0.1)

        # Store model parameters for saving/loading
        self.model_params = {
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "num_layers": self.num_layers,
            "output_size": self.output_size,
            "dropout": self.dropout,
        }

        # Define model layers
        self.lstm = LSTM(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            dropout=self.dropout if self.num_layers > 1 else 0,
            batch_first=True,
        )

        self.linear = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the LSTM model

        Arguments:
        ----------
        x: torch.Tensor
            Input tensor

        Returns:
        --------
        torch.Tensor: Model predictions
        """
        lstm_out, _ = self.lstm(x)
        # Take the last time step output from the LSTM
        out = self.linear(lstm_out[:, -1, :])
        return out

    def save_model(self, path: str) -> None:
        """
        Save the model state

        Arguments:
        ----------
        path: str
            Path to save the model
        """
        super().save_model(path)
