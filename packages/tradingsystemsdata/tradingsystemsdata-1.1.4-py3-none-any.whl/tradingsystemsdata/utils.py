"""
Utility functions

"""
import copy
import datetime as dt
import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay
from tradingsystemsdata.systems_params import system_params_dict
from tradingsystemsdata.marketdata import Markets, NorgateFunctions

class Setup():
    """
    Methods to initialise system
    """
    @staticmethod
    def init_params(inputs: dict) -> dict:
        """
        Initialise parameter dictionary

        Parameters
        ----------
        inputs : Dict
            Dictionary of parameters supplied to the function.

        Returns
        -------
        params : Dict
            Dictionary of parameters.

        """
        # Copy the default parameters
        params = copy.deepcopy(system_params_dict['df_params'])

        # Extract the entry, exit and stop signal dictionaries
        entry_signal_dict = system_params_dict['df_entry_signal_dict']
        exit_signal_dict = system_params_dict['df_exit_signal_dict']
        stop_signal_dict = system_params_dict['df_stop_signal_dict']

        # For all the supplied arguments
        for key, value in inputs.items():

            # Replace the default parameter with that provided
            params[key] = value

        # Set the start and end dates to None if not supplied
        if 'start_date' not in inputs.keys():
            params['start_date'] = None

        if 'end_date' not in inputs.keys():
            params['end_date'] = None

        # Create a list of the entry, exit and stop types
        types = [
            params['entry_type'], params['exit_type'], params['stop_type']]

        # For each parameter in params
        for param in params.keys():

            # If the parameter has not been supplied as an input and it is not
            # the entry exit or stop type
            if (param not in inputs.keys()
                and param not in types):

                # If the parameter takes a specific value for the particular
                # entry type then replace the default with this value
                if param in entry_signal_dict[types[0]].keys():
                    params[param] = entry_signal_dict[types[0]][str(param)]

                if params['exit_type'] is not None:
                    # If the parameter takes a specific value for the
                    # particular exit type then replace the default with this
                    # value
                    if param in exit_signal_dict[types[1]].keys():
                        params[param] = exit_signal_dict[types[1]][str(param)]

                if params['stop_type'] is not None:
                    # If the parameter takes a specific value for the
                    # particular stop type then replace the default with this
                    # value
                    if param in stop_signal_dict[types[2]].keys():
                        params[param] = stop_signal_dict[types[2]][str(param)]

        return params


    @classmethod
    def prepare_data(
        cls,
        params: dict,
        tables: dict,
        market_data: pd.DataFrame | None = None) -> tuple[dict, dict]:
        """
        Get market data ready to be analysed

        Parameters
        ----------
        params : Dict
            Dictionary of parameters.
        tables : Dict
            Dictionary of tables.
        data : DataFrame, optional
            DataFrame of OHLC data. The default is None.

        Returns
        -------
        params : Dict
            Dictionary of parameters.
        tables : Dict
            Dictionary of tables.

        """
        params = cls._prepare_dates(params=params, market_data=market_data)

        params, tables = cls._prepare_ticker_data(
            params=params, tables=tables, market_data=market_data)

        params, tables = cls._prepare_benchmark_data(
            params=params, tables=tables)

        return params, tables


    @staticmethod
    def _prepare_dates(
        params: dict,
        market_data: pd.DataFrame | None = None) -> dict:

        if market_data is None:
            # Set the start and end dates if not provided
            params['start_date'], params['end_date'] = Dates.date_set(
                start_date=params['start_date'], end_date=params['end_date'],
                lookback=params['lookback'])

        else:
            params['start_date'] = str(market_data[0][1].index[0].date())
            params['end_date'] = str(market_data[0][1].index[-1].date())

        return params


    @staticmethod
    def _prepare_ticker_data(
        params: dict,
        tables: dict,
        market_data: pd.DataFrame | None = None) -> tuple[dict, dict]:

        if params['input_data'] == 'reset':
            # Reset the prices and benchmark tables to the source data
            tables, params = Markets.reset_data(tables, params)

        elif params['input_data'] == 'set':
            tables['prices'] = market_data

        else:
            tables['prices'], params = Markets.create_base_data(
                ticker=params['ticker'], source=params['ticker_source'],
                params=params, benchmark_flag=False)

            if params['ticker'][0] == '&':
                params = NorgateFunctions.contract_data(
                    ticker=params['ticker'], prices=tables['prices'],
                    params=params)
            else:
                params['contract_point_value'] = 1

        return params, tables


    @staticmethod
    def _prepare_benchmark_data(
        params: dict,
        tables: dict) -> tuple[dict, dict]:

        # Extract benchmark data for Beta calculation
        print("Ticker source: ", params['ticker_source'])
        if params['ticker_source'] == 'norgate':
            tables['benchmark'], params = Markets.create_base_data(
                ticker=params['norgate_bench_ticker'], source=params['bench_source'],
                params=params, benchmark_flag=True)
        else:
            tables['benchmark'], params = Markets.create_base_data(
                ticker=params['yahoo_bench_ticker'], source='yahoo',
                params=params, benchmark_flag=True)

        return params, tables


class Labels():
    """
    Create labels for the Entry, Exit and Stop Strategies.

    """

    @classmethod
    def strategy_labels(
        cls,
        params: dict,
        default_dict: dict) -> tuple[str, str, str]:
        """
        Create label and price signal for chosen strategy

        Parameters
        ----------
        **kwargs : Various
            The input parameters necessary for the chosen strategy.

        Returns
        -------
        entry_label : Str
            The longname of the entry strategy.
        exit_label : Str
            The longname of the exit strategy.
        stop_label : Str
            The longname of the stop strategy.

        """

        entry_label = cls._entry_label(
            params=params, default_dict=default_dict)

        if params['exit_type'] is None:
            exit_label = entry_label
        else:
            exit_label = cls._exit_label(
                params=params, default_dict=default_dict)

        if params['stop_type'] is None:
            stop_label = 'None'
        else:
            stop_label = cls._stop_label(
                params=params, default_dict=default_dict)

        return entry_label, exit_label, stop_label


    @staticmethod
    def _entry_label(
        params: dict,
        default_dict: dict) -> str:

        # Simple or Exponential Moving Average label
        if params['simple_ma']:
            ma_type_label = 'S'
        else:
            ma_type_label = 'E'


        # Entry labels

        # Double Moving Average Crossover
        if params['entry_type'] == '2ma':

            # Set the entry label
            entry_label = (
                str(params['ma1'])
                +'-, '
                +str(params['ma2'])
                +'-day : '
                +default_dict['df_entry_signal_labels'][params['entry_type']][0]
                +ma_type_label
                +default_dict['df_entry_signal_labels'][params['entry_type']][1]
                )


        # Triple Moving Average Crossover
        elif params['entry_type'] == '3ma':

            # Set the entry label
            entry_label = (
                str(params['ma1'])
                +'-, '
                +str(params['ma2'])
                +'-, '
                +str(params['ma3'])
                +'-day : '
                +default_dict['df_entry_signal_labels'][params['entry_type']][0]
                +ma_type_label
                +default_dict['df_entry_signal_labels'][params['entry_type']][1]
                )


        # Quad Moving Average Crossover
        elif params['entry_type'] == '4ma':

            # Set the entry label
            entry_label = (
                str(params['ma1'])
                +'-, '
                +str(params['ma2'])
                +'-, '
                +str(params['ma3'])
                +'-, '
                +str(params['ma4'])
                +'-day : '
                +default_dict['df_entry_signal_labels'][params['entry_type']][0]
                +ma_type_label
                +default_dict['df_entry_signal_labels'][params['entry_type']][1]
                )


        # Parabolic SAR
        elif params['entry_type'] == 'sar':

            # Set the entry label
            entry_label = (
                str(params['entry_period'])
                +'-day '
                +str(np.round(params['entry_acceleration_factor'] * 100, 1))
                +'% AF '
                +default_dict['df_entry_signal_labels'][params['entry_type']]
                )


        # Channel Breakout, ADX
        elif params['entry_type'] in ['channel_breakout', 'adx']:

            # Set the entry label
            entry_label = (
                str(params['entry_period'])
                +'-day : '
                +default_dict['df_entry_signal_labels'][params['entry_type']]
                )


        # Stochastic Crossover, Stochastic Pop, Stochastic Over Under and
        # Relative Strength Index
        elif params['entry_type'] in [
            'stoch_cross', 'stoch_over_under', 'stoch_pop', 'rsi']:

            # Set the entry label
            entry_label = (
                str(params['entry_period'])
                +'-day '
                +str(params['entry_overbought'])
                +'-'
                +str(params['entry_oversold'])
                +' : '
                +default_dict['df_entry_signal_labels'][params['entry_type']]
                )


        # Commodity Channel Index, Momentum and Volatility
        elif params['entry_type'] in ['cci', 'momentum', 'volatility']:

            # Set the entry label
            entry_label = (
                str(params['entry_period'])
                +'-day '
                +str(int(params['entry_threshold']*100))
                +'% : '
                +default_dict['df_entry_signal_labels'][params['entry_type']]
                )


        # MACD
        elif params['entry_type'] == 'macd':

            # Set the entry label
            entry_label = (
                str(params['macd_params'][0])
                +'-'
                +str(params['macd_params'][1])
                +'-'
                +str(params['macd_params'][2])
                +' : '
                +default_dict['df_entry_signal_labels'][params['entry_type']]
                )

        # Otherwise raise an error
        else:
            raise ValueError("Please enter a valid entry type")


        return entry_label


    @staticmethod
    def _exit_label(
        params: dict,
        default_dict: dict) -> str:

        # Exit labels

        # Parabolic SAR
        if params['exit_type'] == 'sar':

            # Set the exit label
            exit_label = (
                str(params['exit_period'])
                +'-day '
                +str(np.round(params['exit_acceleration_factor'] * 100, 1))
                +'% AF '
                +default_dict['df_exit_signal_labels'][params['exit_type']]
                )


        # Stochastic Crossover and Trailing Relative Strength Index
        elif params['exit_type'] in ['stoch_cross', 'rsi_trail']:

            # Set the exit label
            exit_label = (
                str(params['exit_period'])
                +'-day '
                +str(params['exit_overbought'])
                +'-'
                +str(params['exit_oversold'])
                +' : '
                +default_dict['df_exit_signal_labels'][params['exit_type']]
                )


        # Volatility
        elif params['exit_type'] in ['volatility']:

            # Set the exit label
            exit_label = (
                str(params['exit_period'])
                +'-day '
                +str(int(params['exit_threshold']*100))
                +'% : '
                +default_dict['df_exit_signal_labels'][params['exit_type']]
                )


        # Trailing Stop and Profit Target
        elif params['exit_type'] in ['trailing_stop', 'profit_target']:

            # Set the exit label
            exit_label = (
                '$'
                +str(int(params['exit_amount']))
                +' '
                +default_dict['df_exit_signal_labels'][params['exit_type']]
                )


        # Support/Resistance, Key Reversal Day and n-Day Range
        elif params['exit_type'] in ['sup_res', 'key_reversal', 'nday_range']:

            # Set the exit label
            exit_label = (
                str(params['exit_period'])
                +'-day '
                +default_dict['df_exit_signal_labels'][params['exit_type']]
                )

        # Random exit
        elif params['exit_type'] in ['random']:

            # Set the exit label
            exit_label = (
                default_dict['df_exit_signal_labels'][params['exit_type']]
                +' exit'
                )

        # Otherwise raise an error
        else:
            raise ValueError("Please enter a valid exit type")

        return exit_label


    @staticmethod
    def _stop_label(
        params: dict,
        default_dict: dict) -> str:

        # Stop labels
        # Initial Dollar, Breakeven, Trailing Close and Trailing High Low
        if params['stop_type'] in [
            'initial_dollar', 'breakeven', 'trail_close', 'trail_high_low']:

            # Set the stop label
            stop_label = (
                '$'
                +str(int(params['stop_amount']))
                +' '
                +default_dict['df_stop_signal_labels'][params['stop_type']]
                )

        # Support / Resistance and Immediate Profit
        elif params['stop_type'] in ['sup_res', 'immediate_profit']:

            # Set the stop label
            stop_label = (
                str(params['stop_period'])
                +'-day '
                +default_dict['df_stop_signal_labels'][params['stop_type']]
                )

        # Otherwise raise an error
        else:
            raise ValueError("Please enter a valid stop type")

        return stop_label


    @staticmethod
    def position_size_label(params: dict) -> dict:
        """
        Create position size label

        Parameters
        ----------
        params : Dict
            Dictionary of parameters.

        Returns
        -------
        params : Dict
            Dictionary of parameters.

        """
        if params['position_type'] == 'equity_constant':
            params['position_size_label'] = (
                str(int(params['equity_inv_perc'] * 100))
                +'% Starting Equity / Initial Trade Entry Price'
                )

        elif params['position_type'] == 'equity_variable':
            params['position_size_label'] = (
                str(int(params['equity_inv_perc'] * 100))
                +'% Starting Equity / Trade Entry Price'
                )

        elif params['position_type'] == 'atr':
            params['position_size_label'] = (
                str(params['atr_pos_size'])
                +' day ATR : '
                +str(np.round(params['position_risk_perc'], 2))
                +'% risk'
                )
        else:
            params['position_size_label'] = (
                str(params['fixed_pos_size'])
                +' contracts fixed size'
                )

        return params


class Dates():
    """
    Date calculation and formatting functions.

    """

    @staticmethod
    def date_set(
        start_date: str,
        end_date: str,
        lookback: int) -> tuple[str, str]:
        """
        Create start and end dates if not supplied

        Parameters
        ----------
        start_date : Str, optional
            Date to begin backtest. Format is YYYY-MM-DD. The default is 750
            business days prior (circa 3 years).
        end_date : Str, optional
            Date to end backtest. Format is YYYY-MM-DD. The default is the
            last business day.
        lookback : Int, optional
            Number of business days to use for the backtest. The default is 750
            business days (circa 3 years).

        Returns
        -------
        start_date : Str
            Date to begin backtest. Format is YYYY-MM-DD.
        end_date : Str
            Date to end backtest. Format is YYYY-MM-DD.

        """

        # If end date is not provided, set to previous working day
        if end_date is None:
            end_date_as_dt = (dt.datetime.today() - BDay(1)).date()
            end_date = str(end_date_as_dt)

        # If start date is not provided, set to today minus lookback period
        if start_date is None:
            start_date_as_dt = (dt.datetime.today() -
                                pd.Timedelta(days=lookback*(365/250))).date()
            start_date = str(start_date_as_dt)

        return start_date, end_date


class Reformat():
    """
    Functions for mapping / scaling data
    """

    @staticmethod
    def position_scale(
        pos_dict: dict,
        position_size: pd.Series) -> dict:
        """
        Scale raw positions by position size

        Parameters
        ----------
        raw_pos_dict : Dict
            Dictionary of start of day, end of day positions and trade actions.
        position_size : Series
            Array of the position size to be applied each day.

        Returns
        -------
        scaled_dict : Dict
            Dictionary of the 3 arrays, scaled by the position sizes.

        """

        sod = pos_dict['start_of_day_position']
        tact = pos_dict['trade_action']
        eod = pos_dict['end_of_day_position']
        pos_size = np.array(position_size)
        start_of_day_position = np.array([0] * len(sod), dtype=int)
        trade_action = np.array([0] * len(sod), dtype=int)
        end_of_day_position = np.array([0] * len(sod), dtype=int)

        for row in range(1, len(sod)):
            start_of_day_position[row] = (
                sod[row] * pos_size[row-1]
                )
            if tact[row] != 0:
                trade_action[row] = (
                    (-eod[row-1] * pos_size[row-1]) + (
                        (tact[row] + eod[row-1]) *
                        pos_size[row])
                    )
            end_of_day_position[row] = (
                start_of_day_position[row] + trade_action[row])

        scaled_pos_dict = {}
        scaled_pos_dict['start_of_day_position'] = np.array(
            start_of_day_position)
        scaled_pos_dict['trade_action'] = np.array(trade_action)
        scaled_pos_dict['end_of_day_position'] = np.array(end_of_day_position)

        return scaled_pos_dict


    @staticmethod
    def map_to_prices(
        prices: pd.DataFrame,
        input_dict: dict,
        title_modifier: str) -> pd.DataFrame:
        """
        Map dictionary of arrays to the OHLC data

        Parameters
        ----------
        prices : DataFrame
            The OHLC data.
        input_dict : Dict
            Dictionary of arrays.
        title_modifier : Str
            String to append to the array names.

        Returns
        -------
        prices : DataFrame
            The OHLC data.

        """
        # For each key, value combination in the input dictionary
        for key, value in input_dict.items():

            # Add the array to the OHLC DataFrame appending the title modifier
            # to the beginning of the name
            prices[title_modifier+key] = value

        return prices
