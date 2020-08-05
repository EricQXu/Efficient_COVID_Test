import random
"""
Stopping Condition:
len(splittedlist) == 1 or splittedList.count(False) == len(splittedList)
"""
# N = int(10)
# create = [True, False, True, False, False, False, False, True, False, False]

# def countSplit(create, halves, n, count = 0):
# 	midIndex = len(create) // 2
# 	half1 = create[:midIndex]
# 	half2 = create[midIndex:]
# 	if ((len(half1) == 1 and len(half2) == 1) or (half1.count(False) == len(half1) and half2.count(False) == len(half2))) and (n == 0):
# 		return count
# 	else:
# 		countSplit(create, half1, (n-1), (count+1))
# 		countSplit(create, half2, (n-1), (count+1))
# 		return
#
# print(countSplit(create, 1))

# Creates a list of positive and negative people
def create_patients(N, p, mode):
	if mode == 'random-case':
		# there are p True cases and N-p False cases
		# distributed randomly
		li = []

		for i in range(N - p):
			li.append(False)

		for j in range(p):
			li.insert(random.randint(0, len(li)), True)
		return li
	elif mode == 'at-start-or-end':
		# there are p True cases and N-p False cases
		# distributed at start or at end
		# was called best-case in pre-release builds
		li = []
		fNum = N-p
		for i in range(p):
			li.append(True)
		for i in range(fNum):
			li.append(False)
		return li
	if mode == 'collectively':
		# there are p True cases and N-p False cases
		# distributed consecutively at random places
		li = []
		for i in range(N - p):
			li.append(False)
		pos = random.randint(1, N)
		for i in range(p):
			li.insert(pos - 1, True)
		return li
	elif mode == 'evenly':
		# there are p True cases and N-p False cases
		# distributed evenly
		# was called worst-case in pre-release builds
		def get_frac(applied, total):
			if total == 0:
				assert applied == 0
				frac = 1
			else:
				frac = applied / total
			return frac

		def is_apply_f(applied_f, applied_t):
			f_frac = get_frac(applied_f, N - p)
			t_frac = get_frac(applied_t, p)
			return f_frac < t_frac

		li = []
		applied_f = 0
		applied_t = 0
		while applied_f != N - p or applied_t != p:
			if is_apply_f(applied_f, applied_t):
				li.append(False)
				applied_f += 1
			else:
				li.append(True)
				applied_t += 1
		return li
	elif mode == 'old':
		# old implementation:
		# there are N people; each person has p% chance of being True
		li = []
		for i in range(N):
			if random.random() < p/100:
				li.append(True)
			else:
				li.append(False)
		return li
	else:
		assert False

def run_test(patients):
	return (True in patients)

def split_patients(patients):
	assert len(patients) > 1
	mid_point = len(patients) // 2
	patients_group_list = [patients[:mid_point], patients[mid_point:]]
	return patients_group_list

def our_test_method(patients):
	num_positive = 0
	num_tests = 1
	is_positive = run_test(patients)
	if is_positive:
		num_positive_group, num_tests_group = our_test_method_helper(patients)
		num_positive += num_positive_group
		num_tests += num_tests_group
	else:
		num_positive += len(patients)
	return num_positive, num_tests


def our_test_method_helper(patients):
	if len(patients) > 1:
		num_positive, num_tests = 0, 0
		patients_group_list = split_patients(patients)
		num_tests += len(patients_group_list)
		# uncomment the line below to see how the list is splitted
		# print([len(x) for x in patients_group_list])
		for patients_group in patients_group_list:
			is_positive = run_test(patients_group)
			if is_positive:
				# run test
				num_positive_group, num_tests_group = our_test_method_helper(patients_group)
			else:
				# run test
				num_positive_group, num_tests_group = 0,0
			num_positive += num_positive_group
			num_tests += num_tests_group
	elif len(patients) == 1:
		is_positive = run_test(patients)
		if is_positive:
			num_positive = 1
		else:
			num_positive = 0
		# ran test
		num_tests = 0
	else:
		assert False
	return num_positive, num_tests

def classic_test_method(patients):
	num_positive, num_tests = 0, 0
	for patient in patients:
		is_positive = run_test([patient])
		if is_positive:
			num_positive += 1
		num_tests += 1
	return num_positive, num_tests


N = int(input('How many people are to be tested in total (**PLEASE ENTER AN INTEGER (ex. 100))? '))
p = int(input('What is the probability of COVID-19 in your region/location (**PLEASE ENTER A PERCENTAGE W/O PERCENT SIGN (ex. 5))? '))
mode = input('Which method type (choose between: random-case/at-start-or-end/collectively/evenly/old)? ')

assert mode in ['random-case', 'at-start-or-end', 'collectively', 'evenly', 'old']

patients = create_patients(N, p, mode)
num_positive, num_tests = our_test_method(patients)
num_positive_classic, num_tests_classic = classic_test_method(patients)

print('actual patient list: {}'.format(patients))
print('Our test method found {} positive cases in {} tests.'.format(num_positive, num_tests))
print('The classic test method found {} positive cases in {} tests.'.format(num_positive_classic, num_tests_classic))