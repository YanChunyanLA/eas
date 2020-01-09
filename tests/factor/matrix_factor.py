from eas.factor import MatrixFactor, ConstantMatrixFactor

c = ConstantMatrixFactor(0.5, 3000, 10)
print(MatrixFactor.is_matrix_factor(c))