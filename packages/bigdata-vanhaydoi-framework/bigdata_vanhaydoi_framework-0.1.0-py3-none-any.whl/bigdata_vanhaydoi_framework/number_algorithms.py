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