import functools
import jax
import jax.numpy as jnp
import numpy as np


class RolloutWrapper:

    def __init__(self, env, model_forward=None):
        self.env = env
        self.model_forward = model_forward

    def batch_rollout(self, rng_keys, n_steps, policy_params=None):
        """
        Evaluate a policy on sequential rollouts. The number of sequential rollouts is given by
        the dimensionality of rng_keys.
        todo: use multiprocessing

        """
        all_obs, all_action, all_reward, all_next_obs, all_absorbing, all_done, cum_return = [], [], [], [], [], [], []
        for k in rng_keys:
            (ep_obs, ep_action, ep_reward, ep_next_obs,
             ep_absorbing, ep_done,  ep_cum_return) = self.single_rollout(k, n_steps, policy_params)

            all_obs.append(ep_obs)
            all_next_obs.append(ep_next_obs)
            all_action.append(ep_action)
            all_reward.append(ep_reward)
            all_absorbing.append(ep_absorbing)
            all_done.append(ep_done)
            cum_return.append(ep_cum_return)

        return (np.stack(all_obs), np.stack(all_action), np.stack(all_reward), np.stack(all_next_obs),
                np.stack(all_absorbing), np.stack(all_done), np.stack(cum_return))

    def single_rollout(self, rng_key, n_steps, policy_params=None):
        """Rollout an episode."""
        # Reset the environment
        rng_reset, rng_episode = jax.random.split(rng_key)

        obs = self.env.reset(rng_reset)

        all_obs, all_action, all_reward, all_next_obs, all_absorbing, all_done, cum_return = [], [], [], [], [], [], []
        first_state_in_episode = True

        for i in range(n_steps):

            if self.model_forward is not None:
                action = self.model_forward(obs, **policy_params)
            else:
                rng_episode, rng_action = jax.random.split(rng_episode)
                action = self.env.sample_action_space(rng_action)

            next_obs, reward, absorbing, done, info = self.env.step(action)

            all_obs.append(obs)
            all_next_obs.append(next_obs)
            all_action.append(action)
            all_reward.append(reward)
            all_absorbing.append(absorbing)
            all_done.append(done)
            if first_state_in_episode:
                cum_return.append(reward)
            else:
                cum_return.append(reward + cum_return[-1])

            if done:
                obs = self.env.reset(rng_reset)
                first_state_in_episode = True
            else:
                obs = next_obs
                first_state_in_episode = False

        return (np.array(all_obs), np.array(all_action), np.array(all_reward), np.array(all_next_obs),
                np.array(all_absorbing), np.array(all_done), np.array(cum_return))


class MjxRolloutWrapper:
    """
    This is a rollout wrapper for LocoMuJoCo environments motivated by the gymnax rollout wrapper.
    (https://github.com/RobertTLange/gymnax/blob/main/gymnax/experimental/rollout.py)

    """

    def __init__(self, env, model_forward=None):
        self.env = env
        self.model_forward = model_forward

    @functools.partial(jax.jit, static_argnums=(0, 2))
    def batch_rollout(self, rng_keys, n_steps, policy_params):
        """
        Evaluate a policy on parallel rollouts. The number of parallel rollouts is given by
        the dimensionality of rng_keys.
        """
        batch_rollout = jax.vmap(self.single_rollout, in_axes=(0, None, None))
        return batch_rollout(rng_keys, n_steps, policy_params)

    #@functools.partial(jax.jit, static_argnums=(0, 2))
    def single_rollout(self, rng_key, n_steps, policy_params):
        """Rollout an episode with lax.scan."""
        # Reset the environment
        rng_reset, rng_episode = jax.random.split(rng_key)
        state = self.env.mjx_reset(rng_reset)
        obs = state.observation

        def policy_step(state_input, _):
            """lax.scan compatible step transition in jax env."""
            obs, nstate, policy_params, rng, cum_reward, valid_mask = state_input
            rng, rng_action = jax.random.split(rng, 2)
            if self.model_forward is not None:
                action = self.model_forward(policy_params, obs, rng_action)
            else:
                action = self.env.sample_action_space(rng_action)

            next_state = self.env.mjx_step(nstate, action)
            next_obs = next_state.observation
            reward = next_state.reward
            absorbing = next_state.absorbing
            done = next_state.done

            next_obs = jnp.where(done, next_state.additional_carry.final_observation, next_obs)

            cum_reward = cum_reward + reward * valid_mask
            new_valid_mask = valid_mask * (1 - done)

            carry = [
                next_obs,
                next_state,
                policy_params,
                rng,
                cum_reward,
                new_valid_mask,
            ]
            y = [obs, action, reward, next_obs, absorbing, done, cum_reward]
            return carry, y

        # Scan over episode step loop
        carry_out, scan_out = jax.lax.scan(policy_step,
                                           [obs, state, policy_params, rng_episode,
                                            jnp.float32(0.0), jnp.float32(1.0)], (), n_steps)

        # Return the sum of rewards accumulated by agent in episode rollout
        obs, action, reward, next_obs, absorbing, done, cum_reward = scan_out

        #cum_return = carry_out[-2]
        return obs, action, reward, next_obs, absorbing, done, cum_reward
