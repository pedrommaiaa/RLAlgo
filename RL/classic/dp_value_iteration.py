import sys
import numpy as np

if "../" not in sys.path:
    sys.path.append('../')
np.random.seed(10)
from env.gridWorld import gridWorld


def value_iteration(env, theta=0.0001, discount_factor=1.0):
    """
    Value Iteration Algorithm.

    Args:
        env: OpenAI env. env.P represents the transition probabilities of the environment.
             env.P[s][a] is a list of transition tuples (prob, next_state, reward, done).
             env.nS is the number of states in the environment.
             env.nA is the number of actions in the environment.
        theta: We stop evaluation once our value function change is less than theta for all states.
        discount_factor: Gamma discount factor

    Returns:
        A tuple (policy, V) of the optimal policy and the optimal value function.
    """
    # 1. Init
    V = np.zeros(env.nS)
    while True:
        # Stopping condition
        delta = 0
        # Update each state...
        for s in range(env.nS):
            # Do a one-step lookahead to find the best action
            A = np.zeros(env.nA)
            for a in range(env.nA):
                for prob, next_state, reward, done in env.P[s][a]:
                    A[a] += prob * (reward + discount_factor * V[next_state]) 
            best_action_value = np.max(A)
            # Calculate delta across all states seen so far
            delta = max(delta, np.abs(best_action_value - V[s]))
            # Update the value function. Ref: Sutton book eq. 4.10.
            V[s] = best_action_value
        # Check if we can stop
        if delta < theta:
            break

    # Create a deterministic policy using the optimal value function
    policy = np.zeros([env.nS, env.nA])
    for s in range(env.nS):
        # One step lookahead to find the best action for this state
        A = np.zeros(env.nA)
        for a in range(env.nA):
            for prob, next_state, reward, done in env.P[s][a]:
                A[a] += prob * (reward + discount_factor * V[next_state]) 
        best_action = np.argmax(A)
        # Always take the best action
        policy[s, best_action] = 1.0

    return policy, V


if __name__ == "__main__":

    env = gridWorld()
    policy, v = value_iteration(env)

    print(f"Policy Probability Distribution:\n{policy}\n")

    print(f"Reshaped Grid Policy (0=up, 1=right, 2=down, 3=left):\n{np.reshape(np.argmax(policy, axis=1), env.shape)}\n")

    print(f"Value Function:\n{v}\n")

    print(f"Reshaped Grid Value Function:\n{v.reshape(env.shape)}\n")
