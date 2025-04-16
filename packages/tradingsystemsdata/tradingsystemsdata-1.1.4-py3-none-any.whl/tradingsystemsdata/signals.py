"""
Entry and Exit signals

"""
import numpy as np
import pandas as pd
from tradingsystemsdata.dollar_exits import DollarExit
from tradingsystemsdata.graph_data import GraphData
from tradingsystemsdata.indicator_entries import IndicatorEntry
from tradingsystemsdata.indicator_exits import IndicatorExit
from tradingsystemsdata.ma_entries import MovingAverageEntry
from tradingsystemsdata.positions import Positions
from tradingsystemsdata.trades import Trades
from tradingsystemsdata.utils import Labels, Reformat

class Signals():
    """
    Calculate entry signals

    """

    @classmethod
    def raw_entry_signals(
        cls,
        tables: dict,
        params: dict) -> tuple[dict, dict, dict]:
        """
        Generate the initial raw entry signals, positions and trades

        Parameters
        ----------
        prices : DataFrame
            The OHLC data.
        entry_type : Str, optional
            The entry strategy. The default is '2ma'.
        ma1 : Int, optional
            The first moving average period.
        ma2 : Int, optional
            The second moving average period.
        ma3 : Int, optional
            The third moving average period.
        ma4 : Int, optional
            The fourth moving average period.
        entry_period : Int
            The number of days to use in the entry strategy. The default is 14.
        entry_oversold : Int
            The oversold level to use in the entry strategy.
        entry_overbought : Int
            The overbought level to use in the entry strategy.
        entry_threshold : Float
            The entry threshold used for momentum / volatility strategies.
            The default is 0 for momentum and 1.5 for volatility.
        simple_ma : Bool
            Whether to calculate a simple or exponential moving average. The
            default is True.
        benchmark : Series
            The series of closing prices of the benchmark underlying.
        entry_acceleration_factor : Float
            The acceleration factor used in the Parabolic SAR entry signal.
            The default is 0.02.

        Returns
        -------
        prices : DataFrame
            The OHLC data.
        start : Int
            The first valid row to start calculating trade information from.

        """
        # Generate entry signals
        tables['prices'], params['start'], \
            tables['prices']['raw_trade_signal'] = cls.entry_signal(
                tables=tables, params=params)

        # Calculate initial position info
        raw_pos_dict = Positions.calc_positions(
            prices=tables['prices'],
            signal=tables['prices']['raw_trade_signal'],
            start=params['start'])

        # Generate trade numbers
        tables['prices']['raw_trade_number'] = Trades.trade_numbers(
            prices=tables['prices'],
            end_of_day_position=raw_pos_dict['end_of_day_position'],
            start=params['start'])

        # Set the position size
        tables['prices'], tables['benchmark'], \
            params = Positions.position_size(
                prices=tables['prices'], benchmark=tables['benchmark'],
                params=params)

        # Set the position size label
        params = Labels.position_size_label(params)

        # Scale the position info by the position size
        scaled_pos_dict = Reformat.position_scale(
            pos_dict=raw_pos_dict,
            position_size=tables['prices']['position_size'])

        # Generate initial trade prices
        raw_trade_price_dict = Trades.trade_prices(
            prices=tables['prices'],
            trade_number=tables['prices']['raw_trade_number'])

        # Map the raw positions to the OHLC data
        tables['prices'] = Reformat.map_to_prices(
            prices=tables['prices'],
            input_dict=scaled_pos_dict,
            title_modifier='raw_')

        # Map the raw trade prices to the OHLC data
        tables['prices'] = Reformat.map_to_prices(
            prices=tables['prices'],
            input_dict=raw_trade_price_dict,
            title_modifier='raw_')

        return tables, params, raw_trade_price_dict


    @classmethod
    def entry_signal(
        cls,
        tables: dict,
        params: dict) -> tuple[pd.DataFrame, int, np.ndarray]:
        """
        Calculate trade entry signals

        Parameters
        ----------
        prices : DataFrame
            The OHLC data.
        entry_type : Str, optional
            The entry strategy. The default is '2ma'.
        ma1 : Int, optional
            The first moving average period.
        ma2 : Int, optional
            The second moving average period.
        ma3 : Int, optional
            The third moving average period.
        ma4 : Int, optional
            The fourth moving average period.
        simple_ma : Bool
            Whether to calculate a simple or exponential moving average. The
            default is True.
        entry_period : Int
            The number of days to use in the entry strategy. The default is 14.
        entry_oversold : Int
            The oversold level to use in the entry strategy.
        entry_overbought : Int
            The overbought level to use in the entry strategy.
        entry_threshold : Float
            The entry threshold used for momentum / volatility strategies.
            The default is 0 for momentum and 1.5 for volatility.
        entry_acceleration_factor : Float
            The acceleration factor used in the Parabolic SAR entry signal.
            The default is 0.02.

        Returns
        -------
        prices : DataFrame
            The OHLC data.
        start : Int
            The first valid row to start calculating trade information from.
        signal : Series
            The series of Buy / Sell signals.

        """

        # Double Moving Average Crossover
        if params['entry_type'] == '2ma':
            tables['prices'], start, \
                signal = MovingAverageEntry.entry_double_ma_crossover(
                    prices=tables['prices'],
                    params=params)

        # Triple Moving Average Crossover
        elif params['entry_type'] == '3ma':
            tables['prices'], start, \
                signal = MovingAverageEntry.entry_triple_ma_crossover(
                    prices=tables['prices'],
                    params=params)

        # Quad Moving Average Crossover
        elif params['entry_type'] == '4ma':
            tables['prices'], start, \
                signal = MovingAverageEntry.entry_quad_ma_crossover(
                    prices=tables['prices'],
                    params=params)

        # Parabolic SAR
        elif params['entry_type'] == 'sar':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_parabolic_sar(
                    prices=tables['prices'],
                    acceleration_factor=params['entry_acceleration_factor'])

        # Channel Breakout
        elif params['entry_type'] == 'channel_breakout':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_channel_breakout(
                    prices=tables['prices'],
                    time_period=params['entry_period'])

        # Stochastic Crossover
        elif params['entry_type'] == 'stoch_cross':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_stochastic_crossover(
                    tables['prices'],
                    time_period=params['entry_period'],
                    oversold=params['entry_oversold'],
                    overbought=params['entry_overbought'])

        # Stochastic Over Under
        elif params['entry_type'] == 'stoch_over_under':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_stochastic_over_under(
                    tables['prices'],
                    time_period=params['entry_period'],
                    oversold=params['entry_oversold'],
                    overbought=params['entry_overbought'])

        # Stochastic Pop
        elif params['entry_type'] == 'stoch_pop':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_stochastic_pop(
                    tables['prices'],
                    time_period=params['entry_period'],
                    oversold=params['entry_oversold'],
                    overbought=params['entry_overbought'])

        # Relative Strength Index
        elif params['entry_type'] == 'rsi':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_rsi(
                    tables['prices'],
                    time_period=params['entry_period'],
                    oversold=params['entry_oversold'],
                    overbought=params['entry_overbought'])

        # ADX
        elif params['entry_type'] == 'adx':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_adx(
                    tables['prices'],
                    time_period=params['entry_period'],
                    threshold=params['adx_threshold'])

        # MACD
        elif params['entry_type'] == 'macd':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_macd(
                    tables['prices'],
                    macd_params=(
                        params['fast_ma'], 
                        params['slow_ma'], 
                        params['signal_smooth']
                        )
                    )

        # Commodity Channel Index
        elif params['entry_type'] == 'cci':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_commodity_channel_index(
                    tables['prices'],
                    time_period=params['entry_period'],
                    threshold=params['entry_threshold'])

        # Momentum
        elif params['entry_type'] == 'momentum':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_momentum(
                    tables['prices'],
                    time_period=params['entry_period'],
                    threshold=params['entry_threshold'])

        # Volatility
        elif params['entry_type'] == 'volatility':
            tables['prices'], start, \
                signal = IndicatorEntry.entry_volatility(
                    tables['prices'],
                    time_period=params['entry_period'],
                    threshold=params['entry_threshold'])

        return tables['prices'], start, signal


    @classmethod
    def exit_and_stop_signals(
        cls,
        prices: pd.DataFrame,
        params: dict) -> pd.DataFrame:
        """
        Calculate trade exit and stop signals.

        Parameters
        ----------
        prices : DataFrame
            The OHLC data
        trade_number : Series
            Array of trade numbers.
        end_of_day_position : Series
            The close of day, long/short/flat position.
        sip_price : Bool
            Whether to set the SIP of the Parabolic SAR exit to n-day
            high / low or to the high of the previous trade. The default is
            False.
        exit_type : Str, optional
            The exit strategy. The default is 'trailing_stop'.
        exit_period : Int, optional
            The number of days to use in the exit strategy. The default is 5.
        stop_type : Str, optional
            The stop strategy. The default is 'initial_dollar'.
        stop_period : Int, optional
            The number of days to use in the stop strategy. The default is 5.
        exit_threshold : Float
            The exit threshold used for the volatility strategy.
            The default is 1.
        exit_oversold : Int, optional
            The oversold level to use in the exit strategy.
        exit_overbought : Int, optional
            The overbought level to use in the exit strategy.
        exit_acceleration_factor : Float
            The acceleration factor used in the Parabolic SAR exit signal.
            The default is 0.02.
        exit_trailing_close : Series, optional
            The exit levels for each trade based on the trailing close
        exit_profit_target : Series, optional
            The exit levels for each trade based on a profit target
        stop_initial_dollar_loss : Series, optional
            The stop levels for each trade based on a dollar loss from the
            entry level.
        stop_profit_target : Series, optional
            The stop levels for each trade based on a profit target
        stop_trailing_close : Series, optional
            The stop levels for each trade based on the trailing close
        stop_trailing_high_low : Series, optional
            The stop levels for each trade based on the trailing high / low.

        Returns
        -------
        prices : DataFrame
            The OHLC data

        """
        if params['exit_type'] is not None:
            # Generate the exit signals
            prices, prices['exit_signal'] = cls._exit_signal(
                prices=prices, params=params)
        else:
            prices['exit_signal'] = np.array([0]*len(prices))

        if params['stop_type'] is not None:
            # Generate the stop signals
            prices, prices['stop_signal'] = cls._stop_signal(
                prices=prices, params=params)
        else:
            prices['stop_signal'] = np.array([0]*len(prices))

        return prices


    @classmethod
    def _exit_signal(
        cls,
        prices: pd.DataFrame,
        params: dict) -> tuple[pd.DataFrame, np.ndarray]:
        """
        Calculate trade exit signals.

        Parameters
        ----------
        prices : DataFrame
            The OHLC data
        exit_type : Str, optional
            The exit strategy. The default is 'trailing_stop'.
        exit_period : Int, optional
            The number of days to use in the exit strategy. The default is 5.
        exit_threshold : Float
            The exit threshold used for the volatility strategy.
        trade_number : Series
            Array of trade numbers.
        end_of_day_position : Series
            The close of day, long/short/flat position.
        exit_oversold : Int, optional
            The oversold level to use in the exit strategy.
        exit_overbought : Int, optional
            The overbought level to use in the exit strategy.
        exit_acceleration_factor : Float
            The acceleration factor used in the Parabolic SAR exit signal.
            The default is 0.02.
        sip_price : Bool
            Whether to set the SIP of the Parabolic SAR exit to n-day
            high / low or to the high of the previous trade. The default is
            False.

        Returns
        -------
        prices : DataFrame
            The OHLC data
        exit : Series
            The exit signals.


        prices : DataFrame
            The OHLC data

        """

        # Parabolic SAR Exit
        if params['exit_type'] == 'sar':
            prices, exit_ = IndicatorExit.exit_parabolic_sar(
                prices=prices,
                time_period=params['exit_period'],
                acceleration_factor=params['exit_acceleration_factor'],
                sip_price=params['sip_price'])

        # Support / Resistance Exit
        elif params['exit_type'] == 'sup_res':
            prices, exit_ = IndicatorExit.exit_support_resistance(
                prices=prices,
                time_period=params['exit_period'])

        # Trailing RSI Exit
        elif params['exit_type'] == 'rsi_trail':
            prices, exit_ = IndicatorExit.exit_rsi_trail(
                prices=prices,
                time_period=params['exit_period'],
                oversold=params['exit_oversold'],
                overbought=params['exit_overbought'])

        # Key Reversal Day Exit
        elif params['exit_type'] == 'key_reversal':
            prices, exit_ = IndicatorExit.exit_key_reversal(
                prices=prices,
                time_period=params['exit_period'])

        # Volatility Breakout Exit
        elif params['exit_type'] == 'volatility':
            prices, exit_ = IndicatorExit.exit_volatility(
                prices=prices,
                time_period=params['exit_period'],
                threshold=params['exit_threshold'])

        # Stochastic Crossover Exit
        elif params['exit_type'] == 'stoch_cross':
            prices, exit_ = IndicatorExit.exit_stochastic_crossover(
                prices=prices,
                time_period=params['exit_period'])

        # N-day Range Exit
        elif params['exit_type'] == 'nday_range':
            prices, exit_ = IndicatorExit.exit_nday_range(
                prices=prices,
                time_period=params['exit_period'])

        # Random Exit
        elif params['exit_type'] == 'random':
            prices, exit_ = IndicatorExit.exit_random(
                prices=prices)

        # Trailing Stop Exit
        elif params['exit_type'] == 'trailing_stop':
            prices, exit_ = DollarExit.exit_dollar(
                exit_level='trail_close',
                prices=prices,
                trigger_value=prices['exit_trailing_close'])

        # Profit Target Exit
        elif params['exit_type'] == 'profit_target':
            prices, exit_ = DollarExit.exit_dollar(
                exit_level='profit_target',
                prices=prices,
                trigger_value=prices['exit_profit_target'])

        return prices, exit_


    @classmethod
    def _stop_signal(
        cls,
        prices: pd.DataFrame,
        params: dict) -> tuple[pd.DataFrame, np.ndarray]:
        """
        Calculate trade stop signals

        Parameters
        ----------
        prices : DataFrame
            The OHLC data
        stop_type : Str
            The type of stop to use.
        stop_period : Int
            The length of time for the indicator calculation.
        trade_number : Series
            Array of trade numbers.
        end_of_day_position : Series
            The close of day, long/short/flat position.
        stop_initial_dollar_loss : Series, optional
            The stop levels for each trade based on a dollar loss from the
            entry level.
        stop_profit_target : Series, optional
            The stop levels for each trade based on a profit target
        stop_trailing_close : Series, optional
            The stop levels for each trade based on the trailing close
        stop_trailing_high_low : Series, optional
            The stop levels for each trade based on the trailing high / low.

        Returns
        -------
        prices : DataFrame
            The OHLC data
        stop : Series
            The stop signals.

        """

        # Support / Resistance Stop
        if params['stop_type'] == 'sup_res':
            prices, stop = IndicatorExit.exit_support_resistance(
                prices=prices,
                time_period=params['stop_period'])

        # Immediate Profit Stop
        elif params['stop_type'] == 'immediate_profit':
            prices, stop = IndicatorExit.exit_immediate_profit(
                prices=prices,
                time_period=params['stop_period'])

        # Initial Dollar Loss Stop
        elif params['stop_type'] == 'initial_dollar':
            prices, stop = DollarExit.exit_dollar(
                exit_level='initial',
                prices=prices,
                trigger_value=prices['stop_initial_dollar_loss'])

        # Breakeven Stop
        elif params['stop_type'] == 'breakeven':
            prices, stop = DollarExit.exit_dollar(
                exit_level='breakeven',
                prices=prices,
                trigger_value=prices['stop_profit_target'])

        # Trailing Stop (Closing Price)
        elif params['stop_type'] == 'trail_close':
            prices, stop = DollarExit.exit_dollar(
                exit_level='trail_close',
                prices=prices,
                trigger_value=prices['stop_trailing_close'])

        # Trailing Stop (High / Low Price)
        elif params['stop_type'] == 'trail_high_low':
            prices, stop = DollarExit.exit_dollar(
                exit_level='trail_high_low',
                prices=prices,
                trigger_value=prices['stop_trailing_high_low'])

        return prices, stop


    @staticmethod
    def final_signals(
        params: dict,
        tables: dict) -> dict:
        """
        Concatenate entry, exit and stop signals into a combined signal.

        Parameters
        ----------
        prices : DataFrame
            The OHLC data.
        start : Int
            The first valid row to start calculating trade information from.

        Returns
        -------
        prices : DataFrame
            The OHLC data.

        """
        # Concatenate the Entry, Exit and Stop signals in a single DataFrame
        trade_signals = pd.concat(
            [tables['prices']['raw_trade_signal'],
             tables['prices']['exit_signal'],
             tables['prices']['stop_signal']], axis=1)

        # Generate single combined trade signal
        tables['prices']['combined_signal'] = Trades.signal_combine(
            prices=tables['prices'], start=params['start'],
            end_of_day_position=tables['prices']['raw_end_of_day_position'],
            trade_signals=trade_signals)

        return tables


class CalculateSignalData():
    """
    Generate signals for data api when graph isn't drawn.
    """
    
    @classmethod
    def generate_signals(cls, default_dict, tables, params):
        """
        Generate signals for data api when graph isn't drawn.

        Parameters
        ----------
        params : Dict
            Dictionary of parameters.
        tables : Dict
            Dictionary of tables.

        Returns
        -------
        Updates params with graph_params and signal_dict.

        """
        # Dictionary to store entry signal data
        es_dict = {}

        # Entry labels
        es_dict['entry_signal_labels'] = default_dict[
            'df_entry_signal_labels']

        # Entry signal indicator column names
        es_dict['entry_signal_indicators'] = default_dict[
            'df_entry_signal_indicators']

        graph_params = GraphData.graph_variables(
                prices=tables['prices'], entry_type=params['entry_type'],
                entry_signal_indicators=es_dict['entry_signal_indicators'])
        
        # Create the trade signal points
        signal_dict = GraphData.create_signals(
            prices=tables['prices'], graph_params=graph_params)
        
        indicators = cls._get_indicators(
            params=params, tables=tables, es_dict=es_dict)
        
        trade_data, trade_data_array = cls._get_trades(tables=tables)

        params['es_dict'] = es_dict
        params['graph_params'] = graph_params
        params['signal_dict'] = signal_dict
        params['indicators'] = indicators        
        params['trade_data'] = trade_data        
        params['trade_data_array'] = trade_data_array        

        return params
    
    
    @staticmethod
    def _get_indicators(params, tables, es_dict):
        indicators = {}

        # Remove nan values from prices DataFrame
        tables['prices'] = tables['prices'].bfill()

        # If the entry is Parabolic SAR
        if params['entry_type'] == 'sar':

            # Extract the SAR series from the core DataFrame
            sar_indicator = tables['prices'][
                es_dict['entry_signal_indicators'][params['entry_type']]]
        
            indicators['sar_indicator'] = sar_indicator

        # If the entry is Moving Average
        if params['entry_type'] in ('2ma', '3ma', '4ma'):

            # Extract the moving averages from the core DataFrame
            ma_1 = tables['prices'][es_dict[
                'entry_signal_indicators'][params['entry_type']][0]]
            ma_2 = tables['prices'][es_dict[
                'entry_signal_indicators'][params['entry_type']][1]]
        
            indicators['ma_1'] = ma_1
            indicators['ma_2'] = ma_2

            if params['entry_type'] in ('3ma', '4ma'):
                ma_3 = tables['prices'][es_dict[
                    'entry_signal_indicators'][params['entry_type']][2]]
                
                indicators['ma_3'] = ma_3

                if params['entry_type'] == '4ma':
                    ma_4 = tables['prices'][es_dict[
                        'entry_signal_indicators'][params[
                            'entry_type']][3]]
                
                    indicators['ma_4'] = ma_4

        # If the entry is Channel Breakout
        if params['entry_type'] == 'channel_breakout':

            # Extract the Upper and Lower channel series from the core DataFrame
            lower_channel = tables['prices'][
                es_dict['entry_signal_indicators'][params[
                    'entry_type']][0]]
            upper_channel = tables['prices'][
                es_dict['entry_signal_indicators'][params[
                    'entry_type']][1]]
        
            indicators['lower_channel'] = lower_channel
            indicators['upper_channel'] = upper_channel
        
        # If the entry involves Stochastics
        if 'stoch' in params['entry_type']:

            # Extract the slow k and slow d series from the core DataFrame
            slow_k = tables['prices'][
                es_dict['entry_signal_indicators'][params[
                    'entry_type']][0]]
            slow_d = tables['prices'][
                es_dict['entry_signal_indicators'][params[
                    'entry_type']][1]]
        
            indicators['slow_k'] = slow_k
            indicators['slow_d'] = slow_d
        
        # If the entry is ADX
        if params['entry_type'] == 'adx':

            # Extract the adx, di+ and di- series from the core DataFrame
            adx = tables['prices'][es_dict[
                'entry_signal_indicators'][params[
                    'entry_type']][0]]						
            di_plus = tables['prices'][es_dict[
                'entry_signal_indicators'][params[
                    'entry_type']][1]] 						
            di_minus = tables['prices'][es_dict[
                'entry_signal_indicators'][params[
                    'entry_type']][2]]
            
            indicators['adx'] = adx
            indicators['di_plus'] = di_plus
            indicators['di_minus'] = di_minus

        # If the entry is MACD
        if params['entry_type'] == 'macd':

            # Extract the macd, signal and hist series from the core DataFrame
            macd = tables['prices'][es_dict[
                'entry_signal_indicators'][params[
                    'entry_type']][0]]						
            macd_signal = tables['prices'][es_dict[
                'entry_signal_indicators'][params[
                    'entry_type']][1]] 						
            macd_hist = tables['prices'][es_dict[
                'entry_signal_indicators'][params[
                    'entry_type']][2]]
            
            indicators['macd'] = macd
            indicators['macd_signal'] = macd_signal
            indicators['macd_hist'] = macd_hist

        # If the entry is RSI
        if params['entry_type'] == 'rsi':

            # Extract the RSI series from the core DataFrame
            rsi = tables['prices'][
                es_dict['entry_signal_indicators'][params['entry_type']]]
        
            indicators['rsi'] = rsi
        
        # If the entry is CCI
        if params['entry_type'] == 'cci':

            # Extract the CCI series from the core DataFrame
            cci = tables['prices'][
                es_dict['entry_signal_indicators'][params['entry_type']]]
        
            indicators['cci'] = cci
        
        # If the entry is momentum
        if params['entry_type'] == 'momentum':

            # Extract the momentum series from the core DataFrame
            momentum = tables['prices'][
                es_dict['entry_signal_indicators'][params['entry_type']]]
        
            indicators['momentum'] = momentum
        
        # If the entry is volatility
        if params['entry_type'] == 'volatility':

            # Extract the volatility series from the core DataFrame
            volatility = tables['prices'][
                es_dict['entry_signal_indicators'][params['entry_type']]]
        
            indicators['volatility'] = volatility

        return indicators    
    
    
    @staticmethod
    def _get_trades(tables):
        prices = tables['prices']
        trade_data = {
            'entry_dates': [],
            'entry_prices': [],
            'exit_dates': [],
            'exit_prices': [],
            'position_sizes': [],
            'abs_pos_sizes': [],
            'profits': [],
            'directions': []
            }

        for row in range(1, len(prices)):

            # Trade Entry Details 
            # For each day when a new trade is started
            if (prices['raw_trade_number'].iloc[row] > 
                prices['raw_trade_number'].iloc[row-1]):

                # Add the trade entry date
                trade_data['entry_dates'].append(str(prices.index[row].date()))
                
                # Add the trade entry price
                trade_data['entry_prices'].append(float(
                    prices['Open'].iloc[row]))

                # Add the position size
                trade_data['position_sizes'].append(int(
                    prices['end_of_day_position'].iloc[row]))
                
                # Add the absolute position size    
                trade_data['abs_pos_sizes'].append(abs(int(
                    prices['end_of_day_position'].iloc[row])))
                
                # Add the trade direction
                direction = ('Long' 
                             if prices['end_of_day_position'].iloc[row] > 0 else 'Short')
                trade_data['directions'].append(direction)

            # Trade Exit Details
            # Closing out the previous days trade with no new trade
            if (prices['trade_number'].iloc[row] == 0 
                and prices['trade_number'].iloc[row-1] !=0):
                trade_data['exit_dates'].append(str(prices.index[row-1].date()))
                trade_data['exit_prices'].append(float(
                    prices['Open'].iloc[row-1]))
                trade_data['profits'].append(float(
                    prices['cumulative_trade_pnl'].iloc[row-1]))

            # Closing out the previous days trade and there is a new trade
            elif (prices['trade_number'].iloc[row] == 
                  (prices['trade_number'].iloc[row-1] + 1) 
                  and prices['trade_number'].iloc[row-1] !=0 
                  and row != len(prices)-1):
                trade_data['exit_dates'].append(str(prices.index[row].date()))
                trade_data['exit_prices'].append(float(
                    prices['Open'].iloc[row]))
                trade_data['profits'].append(float(
                    prices['cumulative_trade_pnl'].iloc[row]))

            # On the last day if the previous day was an open trade and this is reversed there needs to be two trade exits
            else:
                if (row == len(prices)-1 
                    and prices['trade_number'].iloc[row] !=0):
                    trade_data['exit_dates'].append(str(
                        prices.index[row].date()))
                    trade_data['exit_dates'].append(str(
                        prices.index[row].date()))
                    trade_data['exit_prices'].append(float(
                        prices['Open'].iloc[row]))
                    trade_data['exit_prices'].append(float(
                        prices['Close'].iloc[row]))
                    trade_data['profits'].append(float(
                        prices['cumulative_trade_pnl'].iloc[row]))
                    trade_data['profits'].append(float(
                        prices['daily_pnl'].iloc[row]))

        trade_data_array = []

        for index, item in enumerate(trade_data['entry_dates']):
            trade_dict = {}
            trade_dict['entry_date'] = item
            trade_dict['entry_price'] = trade_data['entry_prices'][index]
            #try:
            trade_dict['exit_date'] = trade_data['exit_dates'][index]
            trade_dict['exit_price'] = trade_data['exit_prices'][index]
            trade_dict['profit'] = trade_data['profits'][index]
            # except IndexError:
            #     trade_dict['exit_date'] = str(prices.index[-1].date())
            #     trade_dict['exit_price'] = float(prices['Close'].iloc[-1])
            #     trade_dict['profit'] = float(
            #         prices['cumulative_trade_pnl'].iloc[-1])
            trade_dict['position_size'] = trade_data['position_sizes'][index]
            trade_dict['abs_pos_size'] = trade_data['abs_pos_sizes'][index]
            trade_dict['direction'] = trade_data['directions'][index]
            trade_data_array.append(trade_dict)

        return trade_data, trade_data_array 