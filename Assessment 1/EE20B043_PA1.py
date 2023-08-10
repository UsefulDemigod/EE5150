# Programming Assignment 1
# Harisankar K J, EE20B043


import numpy as np
import matplotlib.pyplot as plt


def simulate_queue(lambda_val, mu_val, T):
    # initializing variables
    queue_length = np.zeros(T)
    queue = 0
    sojourn_times = []
    arrival_times = []
    service_times = []

    for t in range(T):
        # Arrival process
        if np.random.rand() < lambda_val:
            queue += 1
            arrival_times.append(t)

        # Service process
        if np.random.rand() < mu_val and queue > 0:
            queue -= 1
            service_times.append(t)

        queue_length[t] = queue

    average_queue_length = np.mean(queue_length)  # finding mean queue length

    # Calculate sojourn times for each customer
    for i in range(len(service_times)):
        sojourn_times.append(service_times[i] - arrival_times[i])

    average_sojourn_time = np.mean(sojourn_times)

    return average_queue_length, average_sojourn_time


# Parameters
lambda_values = np.arange(0.1, 1.1, 0.1)  # ranges of values of arrival time
mu = 0.9
T = 10000

# Lists to store results
average_lengths = []
average_sojourn_times = []

# Simulate the queue for different arrival rates
for lambda_val in lambda_values:
    average_length, average_sojourn_time = simulate_queue(lambda_val, mu, T)
    average_lengths.append(average_length)
    average_sojourn_times.append(average_sojourn_time)

# Plot average queue length against arrival rate
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(lambda_values, average_lengths, marker='o')
plt.xlabel('Arrival Rate (λ)')
plt.ylabel('Average Queue Length')
plt.title('Average Queue Length vs. Arrival Rate')
plt.grid(True)

# Plot average sojourn time against arrival rate
plt.subplot(1, 2, 2)
plt.plot(lambda_values, average_sojourn_times, marker='o')
plt.xlabel('Arrival Rate (λ)')
plt.ylabel('Average Sojourn Time')
plt.title('Average Sojourn Time vs. Arrival Rate')
plt.grid(True)


# Calculate the ratio of average queue length to average sojourn time
ratio_lengths_sojourn_times = np.divide(average_lengths, average_sojourn_times)

# Plot the ratio against arrival rate simulated and theoretical compared
plt.figure(figsize=(6, 4))
plt.xlabel('Arrival Rate (λ)')
plt.ylabel('Avg Queue Length / Avg Sojourn Time')
plt.title('Ratio of Avg Queue Length to Avg Sojourn Time vs. Arrival Rate')
plt.grid(True)

# Perform linear regression to fit the y=mx+c
m, c = np.polyfit(lambda_values, ratio_lengths_sojourn_times, deg=1)

# Generate the fitted line using the obtained coeffratio_lengths_sojourn_timesicients
fitted_line = m * lambda_values + c

# Plot the original data and the fitted line
plt.plot(lambda_values, fitted_line, 'ro--', label="Theoretical")
plt.plot(lambda_values, ratio_lengths_sojourn_times, 'b--', label='simulated')
plt.show()


plt.figure()
n = 1000
theoretical_average_q = []

for lamda in lambda_values:
    p = lamda * (1 - mu) / (mu * (1 - lamda))
    Pi = np.zeros(n + 1)
    Pi[0] = (1 - p) / (1 - p ** (n + 1))
    for i in range(1, n + 1):
        Pi[i] = p ** i * Pi[0]
    # finding expectation under steady state distribution
    E = np.dot(range(n + 1), Pi)
    theoretical_average_q.append(E)

# plotting the values
plt.plot(lambda_values, theoretical_average_q, 'ro-', label='theoretical')
plt.plot(lambda_values, average_lengths, 'b--', label='simulated')
plt.xlabel('lamda')
plt.ylabel('average queue length')
plt.legend()
plt.grid()
plt.show()
