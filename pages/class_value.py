def get_class(classNumber):
    diagnosis_classes = {0: 'Mild', 1: 'Moderate', 2: 'No_DR', 3: 'Proliferate_DR', 4: 'Severe'}
    return diagnosis_classes.get(classNumber)