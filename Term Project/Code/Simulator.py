#The Code:
#Sulaiman A. Alkandari
#209111338

import random
import numpy

#.................................................................class packet
class Packet():
	#initiating instance variables:
	source = 0
	destination = 0
	ACK = False

	def __init__(self, arrival_time, service_start_time, service_time):
		self.arrival_time = arrival_time
		self.service_start_time = service_start_time
		self.service_time = service_time
		self.service_end_time = service_start_time + service_time
		self.delay = self.service_end_time - arrival_time

	#initiating setters:
	def set_source(self, value):
		self.source = value

	def set_destination(self, value):
		self.destination = value
	
	def set_ACK(self, value):
		self.ACK = value

	#initiating getters:
	def get_source(self):
		return self.source

	def get_destination(self):
		return self.destination
	
	def get_ACK(self):
		return self.ACK

#.......................................................................class sender

class Sender():
	# initiating the instance variables:
	retransmit = False
	address = 0
	out_queue = []
	in_queue = []
	window_size = 1
	window_increment = 1
	threshold = 16
	check_inorder_ACK = [ 0 for i in range(100)]

	#initialize a constructor:
	def __init__(self, address):
		self.address = address
		self.window_size = 1
		self.threshold = 16
	#end of constructor

	#generate setters:
	def set_retransmit(self, value):
		self.retransmit = value

	def set_address(self, value):
		self.address = value

	def set_out_queue(self, value):
		self.out_queue.append(value)

	def set_in_queue(self, value):
		self.in_queue.append(value)

	def set_window_size(self, value):
		self.window_size = value

	def set_threshold(self, value):
		self.threshold = value

	def set_window_increment(self, value):
		self.window_increment = value

	#generate getters:
	def get_retransmit(self):
		return self.retransmit

	def get_address(self):
		return self.address

	def get_out_queue(self):
		return self.out_queue

	def get_in_queue(self):
		return self.in_queue

	def get_window_size(self):
		return self.window_size

	def get_threshold(self):
		return self.threshold

	def get_window_increment(self):
		return self.window_increment

#.........................................................................class Receiver
class Receiver():

	#initiating instance variables:
	ACK_value = 0
	receiver_queue = []

	# initiating setters
	def set_ACK_value(self, value):
		self.ACK_value = value

	def set_receiver_queue(self, value):
		self.receiver_queue.append(value)

	#initiating getters:
	def get_ACK_value(self):
		return self.ACK_value

	def get_receiver_queue(self):
		return self.receiver_queue

#....................................................................class Router
class Router():

	#initiating instance variables
	number_of_lost_packets = 0
	expected_packets_in_queue = []
	droped_packets_queue = []
	average_delay_time_in_queue = []
	expected_utilization = []
	router_queue = []

	#generate setters:
	def set_number_of_lost_packets(self, value):
		self.number_of_lost_packets = value

	def set_expected_packets_in_queue(self, value):
		self.expected_packets_in_queue.append(value)

	def set_droped_packets_queue(self, value):
		self.droped_packets_queue.append(value)

	def set_average_delay_time_in_queue(self, value):
		self.average_delay_time_in_queue.append(value)

	def set_expected_utilization(self, value):
		self.expected_utilization.append(value)

	def set_router_queue(self, value):
		self.router_queue.append(value)

	#generate getters:
	def get_number_of_lost_packets(self):
		return self.number_of_lost_packets

	def get_expected_packets_in_queue(self):
		return self.expected_packets_in_queue

	def get_droped_packets_queue(self):
		return self.droped_packets_queue

	def get_average_delay_time_in_queue(self):
		return self.average_delay_time_in_queue

	def get_expected_utilization(self):
		return self.expected_utilization

	def get_router_queue(self):
		return self.router_queue


#the simulation part....................................................................

sender = Sender(1)
router = Router()
receiver = Receiver()
sender.set_threshold(16)

# lambda, and meu:
lam = 8.0 
meu = 10.0 
rough = lam / meu
probability_zero = (1.0 - rough) / (1.0 - pow(rough, 30))
total_packets = 0.0
droped_packets = 0.0

time = 0
end_time = 5000  
arrival_time = 0
N = 35

while time <= end_time:
	#generating packets step
	##############################################
	for i in range(0, sender.get_window_size()):
		if len(receiver.get_receiver_queue()) == 0:
			arrival_time += numpy.random.poisson(lam)
			service_start_time = arrival_time
			service_time = random.expovariate(meu)
			sender.set_in_queue(Packet(arrival_time, service_start_time, service_time))
			probability_n = pow(rough, len(sender.get_in_queue())) * probability_zero
			router.set_expected_utilization(1.0 - probability_n)
			total_packets += 1
		if len(receiver.get_receiver_queue()) != 0:
			if len(sender.get_in_queue()) == 0:
				arrival_time += numpy.random.poisson(lam)
				service_start_time = max(arrival_time, (receiver.get_receiver_queue()[-1].service_end_time))
				service_time = random.expovariate(meu)
				sender.set_in_queue(Packet(arrival_time, service_start_time, service_time))
				probability_n = pow(rough, len(sender.get_in_queue())) * probability_zero
				router.set_expected_utilization(1.0 - probability_n)
				total_packets += 1
			else:
				arrival_time += numpy.random.poisson(lam)
				service_start_time = max(arrival_time, sender.get_in_queue()[-1].service_end_time)
				service_time = random.expovariate(meu)
				sender.set_in_queue(Packet(arrival_time, service_start_time, service_time))
				probability_n = pow(rough, len(sender.get_in_queue())) * probability_zero
				router.set_expected_utilization(1.0 - probability_n)
				total_packets += 1
	##############################################
	
	for j in range(0, N): 
		if len(sender.get_in_queue()) != 0:
			router.set_router_queue(sender.get_in_queue().pop(0))
		else:
			break
	#..............

	router.set_expected_packets_in_queue(len(router.get_router_queue()))

	if len(sender.get_in_queue()) != 0:
		sender.set_retransmit(True)
		router.set_droped_packets_queue(len(sender.get_in_queue()))
		sender.set_window_size(1)
		sender.set_window_increment(1)
		droped_packets += len(sender.get_in_queue())
	else:
		if sender.get_window_size() <= sender.get_threshold():
			sender.set_window_size(pow(2, sender.get_window_increment()))
			router.set_droped_packets_queue(0)
		else: 
			sender.set_window_size(sender.get_window_size() + 1)
			router.set_droped_packets_queue(0)
	#..............

	for z in range(0, N): 
		if len(router.get_router_queue()) != 0:
			receiver.set_receiver_queue(router.get_router_queue().pop(0))

	for i in range(0, len(sender.get_in_queue())):
		sender.get_in_queue().pop(0)

	#this is to check the progress on window size:
	sender.set_out_queue(sender.get_window_size())
	sender.set_window_increment(sender.get_window_increment() + 1)
	#incrementing the time of arrival by poisson(lambda)
	time += arrival_time
#end while loop

#calculating the statistics
ls = ((rough) / ((1.0 - rough) * (1.0 - pow(rough, (N + 1))))) * ((1.0 + (N * pow(rough, (N + 1)))) - ((N + 1) * pow(rough, N)))
probability_N = pow(rough, N) * probability_zero
lam_eff = lam * (1 - probability_N)
ws = ls / lam_eff
wq = ws - (1.0/meu)
lq = lam * wq
dp = droped_packets / total_packets
u = 1.0 - probability_zero

#...........testing my results..................#
print '..........................((arrival time)).........................'
for i in receiver.get_receiver_queue(): print i.arrival_time
print '..........................((delay)).........................'
for i in receiver.get_receiver_queue(): print i.delay
print '..........................((lost packets)).........................'
for i in router.get_droped_packets_queue(): print i
print '..........................((window progress)).........................'
for i in sender.get_out_queue(): print i
print '..........................((expected packets in queue)).........................'
for i in router.get_expected_packets_in_queue(): print i
print '..........................((service end time)).........................'
for i in receiver.get_receiver_queue(): print i.service_end_time
print '..........................((Expected utilization)).........................'
for i in router.get_expected_utilization(): print i

print '\n\n\n'

#printing the statistics:
print 'The statistics: \n'
print 'The probability that the server is idle: ' + str(probability_zero) 
print 'The probability that the server is full and cannot take any user: ' + str(probability_N)
print 'The expected packets in system: ' + str(ls) 
print 'The value of lambda effective: ' + str(lam_eff)
print 'The expected waiting time in system: ' + str(ws)
print 'The expected waiting time in queue: ' + str(wq)
print 'The expected packets in queue: ' + str(lq)
print 'The dropping probability: ' + str(dp)
print 'The expected utilization: ' + str(u)

#writing the data on a matlab file:
with open('Simulation_Results.m','w') as mat:
	mat.write('arrival_time = [')
	for i in receiver.get_receiver_queue(): mat.write(str(i.arrival_time) + ' ')
	mat.write(']; \n')
	
	mat.write('delay = [')
	for i in receiver.get_receiver_queue(): mat.write(str(i.delay) + ' ')
	mat.write(']; \n')

	mat.write('congestion_window_size = [')
	for i in sender.get_out_queue(): mat.write(str(i) + ' ')
	mat.write(']; \n')

	mat.write('service_end_time = [')
	for i in receiver.get_receiver_queue(): mat.write(str(i.service_end_time) + ' ')
	mat.write(']; \n')

	mat.write('service_start_time = [')
	for i in receiver.get_receiver_queue(): mat.write(str(i.service_start_time) + ' ')
	mat.write(']; \n')

	mat.write('expected_utilization = [')
	for i in router.get_expected_utilization(): mat.write(str(i) + ' ')
	mat.write(']; \n')

	mat.write('subplot(1, 3, 1); \n')
	mat.write('plot(congestion_window_size, \'Color\', \'m\'); \n')
	mat.write('xlabel(\'Time\') \n')
	mat.write('ylabel(\'Congestion Window Size\') \n')
	mat.write('title(\'The Congistion Window Plot\', \'FontSize\', 12) \n')
	mat.write('subplot(1, 3, 2); \n')
	mat.write('plot(expected_utilization, \'Color\', \'b\'); \n')
	mat.write('xlabel(\'Time\') \n')
	mat.write('ylabel(\'Probability\') \n')
	mat.write('title(\'The Utilization\', \'FontSize\', 12) \n')
	mat.write('subplot(1, 3, 3); \n')
	mat.write('plot(delay, \'Color\', \'r\'); \n')
	mat.write('xlabel(\'Time\') \n')
	mat.write('ylabel(\'Waiting Time in Queue\') \n')
	mat.write('title(\'Delay in Queue\', \'FontSize\', 12) \n')
	
