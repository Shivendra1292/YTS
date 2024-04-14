def calculate_ratio(a, ratio):
    # Calculate the ratio
    ratio_b = a * ratio[1] / ratio[0]
    
    return ratio_b

# Input a from the user
a = float(input("Enter value for 'a': "))

# Desired ratio
desired_ratio = (166, 3)

# Calculate b according to the ratio
b = calculate_ratio(a, desired_ratio)

print(f"The value of 'b' according to the ratio {desired_ratio[0]}:{desired_ratio[1]} is {b}")
