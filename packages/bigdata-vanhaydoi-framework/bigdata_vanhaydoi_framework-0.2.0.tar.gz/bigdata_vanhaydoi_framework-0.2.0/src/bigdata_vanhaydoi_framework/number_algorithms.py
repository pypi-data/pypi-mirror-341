class NumberAlgorithm:

    @staticmethod
    def get_max_number(numbers: list) -> int:
        if not numbers:
            raise ValueError("The list of number is empty")
        return max(numbers)
    
    @staticmethod
    def get_min_number(numbers: list) -> int:
        if not numbers:
            raise ValueError("The list of number is empty")
        return min(numbers)
    
    @staticmethod
    def get_average(numbers: list) -> int:
        if not numbers:
            raise ValueError("The list of number is empty")
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def get_median(numbers: list) -> float:
        if not numbers:
            raise ValueError("The list of number is empty")
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2.0
        else:
            return sorted_numbers[mid]