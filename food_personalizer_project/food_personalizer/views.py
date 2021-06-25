from django.shortcuts import render

# Create your views here.
import numpy as np
import django

def pull_arm(arm, successes, total_pulls, prob):
  reward = np.random.choice([0,1], p=[1-prob, prob])
  if reward == 1:
    successes[arm] += 1
  total_pulls[arm] += 1

  return successes, total_pulls

def TS(prob_1, prob_2, horizon, results):
  successes = [1,1]
  total_pulls = [1,1]

  for time in range(horizon):
    arm1 = np.random.beta(1+successes[0], 1+total_pulls[0]-successes[0])
    arm2 = np.random.beta(1+successes[1], 1+total_pulls[1]-successes[1])

    if arm1 > arm2:
      successes, total_pulls = pull_arm(0, successes, total_pulls, prob_1)
      results[time] = 1
    elif arm1 == arm2:
      random_choice = random.choice([0,1])
      if random_choice == 0:
        results[time] = 1
      prob = [prob_1, prob_2]
      successes, total_pulls = pull_arm(random_choice, successes, total_pulls, prob[random_choice])
    else:
      successes, total_pulls = pull_arm(1, successes, total_pulls, prob_2)
    # print(int(arm2>arm1)+1)
  return results

def evaluate_TS(prob_1, prob_2, horizon, num_simulations):
  final_results = np.zeros(horizon)
  for i in range(num_simulations):
    results = np.zeros(horizon)
    results = TS(prob_1, prob_2, horizon, results)
    final_results += results
  final_results /= num_simulations

  return final_results


def TSPostdiff(prob_1, prob_2, horizon, results, c):
  successes = [1,1]
  total_pulls = [1,1]

  for time in range(horizon):
    arm1 = np.random.beta(1+successes[0], 1+total_pulls[0]-successes[0])
    arm2 = np.random.beta(1+successes[1], 1+total_pulls[1]-successes[1])
    difference = np.abs(arm1 - arm2)

    if difference < c:
      random_choice = random.choice([0,1])
      if random_choice == 0:
        results[time] = 1
      prob = [prob_1, prob_2]
      successes, total_pulls = pull_arm(random_choice, successes, total_pulls, prob[random_choice])
    elif arm1 > arm2:
      successes, total_pulls = pull_arm(0, successes, total_pulls, prob_1)
      results[time] = 1
    else:
      successes, total_pulls = pull_arm(1, successes, total_pulls, prob_2)
      # print(int(arm2>arm1)+1)
  return results

def evaluate_TSPostdiff(prob_1, prob_2, horizon, num_simulations, c):
  final_results = np.zeros(horizon)
  for i in range(num_simulations):
    results = np.zeros(horizon)
    results = TSPostdiff(prob_1, prob_2, horizon, results, c)
    final_results += results
  final_results /= num_simulations
  return final_results

