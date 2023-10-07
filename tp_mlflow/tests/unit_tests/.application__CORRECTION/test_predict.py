import unittest
from unittest.mock import patch, Mock, MagicMock
from click.testing import CliRunner
from foodcast.application.predict import predict


class TestPredict(unittest.TestCase):

    @patch('foodcast.application.predict.mlflow_log_pandas')
    @patch('foodcast.application.predict.mlflow_log_plotly')
    @patch('foodcast.application.predict.plotly_predictions')
    @patch('foodcast.application.predict.pd.read_csv')
    @patch('foodcast.application.predict.get_run')
    @patch('foodcast.application.predict.mlflow.pyfunc')
    @patch('foodcast.application.predict.mlflow')
    def test_predict(
        self,
        mock_mlflow: MagicMock,
        mock_pyfunc: MagicMock,
        mock_get_run: MagicMock,
        mock_read_csv: MagicMock,
        mock_plotly_predictions: MagicMock,
        mock_mlflow_log_plotly: MagicMock,
        mock_mlflow_log_pandas: MagicMock
    ) -> None:
        mock_run = MagicMock()
        mock_model = Mock()
        mock_model.predict.return_value = Mock()
        mock_pyfunc.load_model.return_value = mock_model
        mock_mlflow.start_run.return_value = mock_run
        mock_get_run.return_value.info.artifact_uri = 'uri'
        runner = CliRunner()
        result = runner.invoke(predict, ['--next-week', '10'])
        assert result.exit_code == 0
        mock_mlflow.start_run.assert_called_once()
        mock_run.__enter__.assert_called_once()
        mock_run.__exit__.assert_called_once()
        mock_mlflow.log_params.assert_called()
        mock_get_run.assert_called()
        mock_pyfunc.load_model.assert_called()
        mock_read_csv.assert_called()
        mock_model.predict.assert_called()
        mock_plotly_predictions.assert_called()
        mock_mlflow_log_plotly.assert_called()
        mock_mlflow_log_pandas.assert_called()
