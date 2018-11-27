'''
@author: Justin Wei

We learned about hashing IP addresses in my algorithms course. This is an
empirical test of the method used to hash IP addresses that I made while bored on a plane

Some results I found:

Finding rate of collisions given 1000000 hashes...
Empirical collision rate: 0.00389
Expected collision rate:  0.00389

Simulating hashing 1000000 elements into 257 buckets...
There were 0 empty buckets.
On average, the 257 filled buckets had 3891.05 elements
If the elements were uniformly distributed, we would expect 3891.00 elements per bucket


@todo: Make hashing function general to other types of objects, not just integers for IP addresses
@todo: Implement nearest prime
@todo: Implement lazy lists/generators instead of list-comprehensions for large lists like random ip address list
'''

import random
import pprint as pprint

def generate_hash_fn(n,num_a_vals):
    # returns a hash function
    # n = 257 and num = 4 for ip addresses
    a_vals = [random.randint(0,n-1) for _ in range(num_a_vals)]
    def hash_fn(ip):
        eight_bit_nums = map(int, ip.split('.'))
        return sum(eight_bit * a for eight_bit, a in zip(eight_bit_nums, a_vals)) % n
    return hash_fn, a_vals

def generate_random_ip():
    # returns a random ip address in form of four eight-bit numbers joined by .
    # i.e. "123.45.6.78"
    nums = [str(random.randint(0,256)) for _ in range(4)]
    return '.'.join(nums)

def generate_random_ip_list(num):
    # return list of ip addresses
    return [generate_random_ip() for _ in range(num)]

def nearest_prime(num_elements):
    # returns the nearest prime number greater than num_buckets
    # generally for best performance you want the size of hash table to be about twice as large as number of items
    # however this works for now
    return 257

def summarize(counts):
    total, num_filled_buckets, num_empty_buckets = 0, 0, 0
    for bucket, count in counts.items():
        total += count
        if count == 0: num_empty_buckets += 1
        else: num_filled_buckets += 1
        
    print('There were %d empty buckets.' % (num_empty_buckets))
    average_filled = float(total) / float(num_filled_buckets)
    print('On average, the %d filled buckets had %0.2f elements' % (num_filled_buckets, average_filled))
    print('If the elements were uniformly distributed, we would expect %0.2f elements per bucket' % (num_elements / num_buckets))

def test_hash_rate(num_buckets, n, hash_fn, num_trials):
    print("Finding rate of collisions given %d hashes..." % (num_trials))
    h_a_x = hash_fn(generate_random_ip())
    collisions = sum(1 if h_a_x == hash_fn(generate_random_ip()) else 0 for _ in range(num_trials))
    collision_rate = float(collisions) / float(num_trials)
    print("Empirical collision rate: %.5f\nExpected collision rate:  %.5f" % (collision_rate, float(1)/n))
    
def simulate(num_buckets, num_elements, hash_fn, show_buckets=False):
    # simulates hashing num_elements random items into num_buckets buckets
    # optional parameter show_buckets allows you to visualize which elements were hashed to which buckets
    print('Simulating hashing %d elements into %d buckets...' % (num_elements, num_buckets))
    ip_list = generate_random_ip_list(num_elements)

    # buckets is meant to simulate an array of size num_buckets
    # we fill in the empty values later
    buckets,counts = {i: [] for i in range(num_buckets)}, {i: 0 for i in range(num_buckets)}

    for ip in ip_list:
        b = hash_fn(ip)
        buckets[b] = buckets[b] + [ip] 
        counts[b] = counts[b] + 1

    # display information
    if show_buckets: pprint.pprint(buckets)
    summarize(counts)
    
if __name__ == '__main__':
    num_elements = 10**6
    num_buckets = n = nearest_prime(num_elements) 
    hash_fn, a_values = generate_hash_fn(n,4)
    print('Given %d buckets and a nearest prime number of %d, our hash function uses a-values %s\n' % (num_buckets, n, str(a_values)))

    num_trials = 10**6
    test_hash_rate(num_buckets, n, hash_fn, num_trials)
    print('')
    simulate(num_buckets, num_elements, hash_fn, show_buckets=False)

    