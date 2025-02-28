"""
Reinforcement Learning agent for trading policy optimization.

This module implements RL agents (DQN, PPO) that learn optimal trading
policies through trial and error, taking actions (buy, sell, hold) in
an environment (market data) to maximize rewards (profits).
"""
import os
import numpy as np
import pandas as pd
import gym
from gym import spaces
from stable_baselines3 import PPO, DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
import logging

logger = logging.getLogger(__name__)

class TradingEnvironment(gym.Env):
    """Custom Trading Environment that follows gym interface."""
    
    metadata = {'render.modes': ['human']}
    
    def __init__(self, df, initial_balance=10000, transaction_fee=0.001, window_size=60):
        """Initialize the trading environment."""
        super(TradingEnvironment, self).__init__()
        
        self.df = df
        self.initial_balance = initial_balance
        self.transaction_fee = transaction_fee
        self.window_size = window_size
        
        # Define action and observation space
        # Actions: 0 = Hold, 1 = Buy, 2 = Sell
        self.action_space = spaces.Discrete(3)
        
        # Observation space: [market_data (window_size * features), balance, position]
        # Features: OHLCV + technical indicators
        self.n_features = df.shape[1]
        self.observation_space = spaces.Box(
            low=-np.inf, 
            high=np.inf, 
            shape=(self.window_size * self.n_features + 2,),
            dtype=np.float32
        )
        
        # Initialize state
        self.reset()
    
    def reset(self):
        """Reset the environment to initial state."""
        self.current_step = self.window_size
        self.balance = self.initial_balance
        self.position = 0  # 0 = no position, positive = long position
        self.done = False
        self.history = []
        
        return self._get_observation()
    
    def step(self, action):
        """Take a step in the environment."""
        # Get current price
        current_price = self.df.iloc[self.current_step]['close']
        
        # Execute action
        reward = 0
        if action == 1:  # Buy
            if self.position == 0:  # Only buy if we don't have a position
                shares = self.balance / current_price
                cost = shares * current_price * (1 + self.transaction_fee)
                if cost <= self.balance:
                    self.position = shares
                    self.balance -= cost
                    reward = 0  # Neutral reward for opening position
        
        elif action == 2:  # Sell
            if self.position > 0:  # Only sell if we have a position
                sale_value = self.position * current_price * (1 - self.transaction_fee)
                self.balance += sale_value
                # Calculate profit/loss as reward
                cost_basis = self.initial_balance - self.balance
                reward = (sale_value - cost_basis) / cost_basis  # Percentage return
                self.position = 0
        
        # Move to next step
        self.current_step += 1
        
        # Calculate portfolio value
        portfolio_value = self.balance + (self.position * current_price if self.position > 0 else 0)
        
        # Check if episode is done
        if self.current_step >= len(self.df) - 1:
            self.done = True
            # If we still have a position, sell it
            if self.position > 0:
                sale_value = self.position * current_price * (1 - self.transaction_fee)
                self.balance += sale_value
                self.position = 0
        
        # Record history for rendering
        self.history.append({
            'step': self.current_step,
            'action': action,
            'price': current_price,
            'balance': self.balance,
            'position': self.position,
            'portfolio_value': portfolio_value,
            'reward': reward
        })
        
        # Get observation, reward, done, info
        observation = self._get_observation()
        info = {
            'portfolio_value': portfolio_value,
            'balance': self.balance,
            'position': self.position
        }
        
        return observation, reward, self.done, info
    
    def _get_observation(self):
        """Get the current observation."""
        # Get window of market data
        market_data = self.df.iloc[self.current_step - self.window_size:self.current_step].values.flatten()
        
        # Combine market data with account state
        observation = np.append(market_data, [self.balance, self.position])
        
        return observation
    
    def render(self, mode='human'):
        """Render the environment."""
        if mode == 'human':
            # Implementation details...
            pass
        
        return None


class TradingCallback(BaseCallback):
    """Callback for logging training progress."""
    
    def __init__(self, verbose=0):
        """Initialize the callback."""
        super(TradingCallback, self).__init__(verbose)
        self.rewards = []
        self.portfolio_values = []
    
    def _on_step(self):
        """Called at each step of training."""
        # Implementation details...
        return True


class RLTradingAgent:
    """Reinforcement Learning agent for trading."""
    
    def __init__(self, 
                 algorithm='ppo', 
                 policy='MlpPolicy',
                 learning_rate=0.0003,
                 n_steps=2048,
                 batch_size=64,
                 n_epochs=10,
                 gamma=0.99,
                 model_dir='models/rl'):
        """Initialize the RL trading agent."""
        self.algorithm = algorithm
        self.policy = policy
        self.learning_rate = learning_rate
        self.n_steps = n_steps
        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.gamma = gamma
        self.model_dir = model_dir
        self.model = None
        
        # Create model directory if it doesn't exist
        os.makedirs(model_dir, exist_ok=True)
    
    def create_environment(self, df, **kwargs):
        """Create a trading environment."""
        env = TradingEnvironment(df, **kwargs)
        env = Monitor(env)
        env = DummyVecEnv([lambda: env])
        return env
    
    def build_model(self, env):
        """Build the RL model."""
        if self.algorithm.lower() == 'ppo':
            model = PPO(
                self.policy, 
                env, 
                learning_rate=self.learning_rate,
                n_steps=self.n_steps,
                batch_size=self.batch_size,
                n_epochs=self.n_epochs,
                gamma=self.gamma,
                verbose=1
            )
        elif self.algorithm.lower() == 'dqn':
            model = DQN(
                self.policy,
                env,
                learning_rate=self.learning_rate,
                buffer_size=10000,
                learning_starts=1000,
                batch_size=self.batch_size,
                gamma=self.gamma,
                verbose=1
            )
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        self.model = model
        logger.info(f"Built {self.algorithm.upper()} model with {self.policy} policy")
        return model
    
    def train(self, env, total_timesteps=100000, callback=None):
        """Train the RL model."""
        if self.model is None:
            self.build_model(env)
        
        if callback is None:
            callback = TradingCallback()
        
        self.model.learn(total_timesteps=total_timesteps, callback=callback)
        logger.info(f"Trained {self.algorithm.upper()} model for {total_timesteps} timesteps")
        return self.model
    
    def predict(self, observation):
        """Make a prediction using the trained model."""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        action, _states = self.model.predict(observation)
        return action
    
    def save_model(self, filepath=None):
        """Save the trained model."""
        if self.model is None:
            raise ValueError("No model to save")
        
        if filepath is None:
            filepath = os.path.join(self.model_dir, f"{self.algorithm}_trading_model")
        
        self.model.save(filepath)
        logger.info(f"Saved {self.algorithm.upper()} model to {filepath}")
        return filepath
    
    def load_model(self, filepath=None):
        """Load a trained model."""
        if filepath is None:
            filepath = os.path.join(self.model_dir, f"{self.algorithm}_trading_model")
        
        if self.algorithm.lower() == 'ppo':
            self.model = PPO.load(filepath)
        elif self.algorithm.lower() == 'dqn':
            self.model = DQN.load(filepath)
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
        
        logger.info(f"Loaded {self.algorithm.upper()} model from {filepath}")
        return self.model
