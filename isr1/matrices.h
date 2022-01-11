#ifndef MATRICES_H
#define MATRICES_H

struct matrix
{
	int length;
	int *vals;
	int rows;
	int cols;
};

struct matrix *gen_matrix(int rows, int cols);
void free_matrix(struct matrix *A);
void print_matrix(struct matrix *A);

struct matrix *matrix_mult(struct matrix *A, struct matrix *B);
struct matrix *scalar_mult(int num, struct matrix *A);
struct matrix *add_matrices(struct matrix *A, struct matrix *B, char sign);

struct matrix *gen_unit_matrix(int rows, int cols);
void randomize_matrix(struct matrix *A);

struct matrix *transpose(struct matrix *A);

void del_row(struct matrix *A, int krow);

#endif
