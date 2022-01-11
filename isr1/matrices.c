#include "stdio.h"
#include "stdlib.h"
#include "./matrcies.h"

/*
 * Multiply matrices.
 * Return the newly allocated resulting matrix.
 * If multiplication isn't possible or there is another fault, return NULL.
 */
struct matrix *matrix_mult(struct matrix *A, struct matrix *B)
{
    if (A->cols != B->rows)
    {
        return NULL;
    }

    struct matrix *result = gen_matrix(A->rows, B->cols); // allocate
    for (int row = 0; row < A->rows; row++)
    {
        for (int colRight = 0; colRight < B->cols; colRight++) // right matrix
        {
            int *p_el = result->vals + B->cols * row + colRight; // to the current element of the matrix
            *p_el = 0;
            for (int colLeft = 0; colLeft < A->cols; colLeft++)
            {
                *p_el += *(A->vals + A->cols * row + colLeft) * *(B->vals + colLeft * B->cols + colRight);
            }
        }
    }
    return result;
}

/*
 * Multiply every element of the matrix.
 */
struct matrix *scalar_mult(int num, struct matrix *A)
{
    struct matrix *result = gen_matrix(A->rows, A->cols);

    for (int i = 0; i < A->rows * A->cols; i++)
    {
        int *p_mel = A->vals + i;      // matrix element
        int *p_rel = result->vals + i; // result element
        *p_rel = num * *(p_mel);
    }
    return result;
}

/*
 * Generate a unary matrix.
 */
struct matrix *gen_unit_matrix(int rows, int cols)
{
    struct matrix *result = gen_matrix(rows, cols);
    for (int row = 0; row < rows; row++)
    {
        for (int col = 0; col < cols; col++)
        {
            int *p_el = result->vals + row * cols + col;
            if (row == col)
                *p_el = 1;
            else
                *p_el = 0;
        }
    }
    return result;
}

/**
 * Get the scalar sum of the matrices.
 * The sign parameters can be '-' or '+'. It defines the operation.
 * If matrices differ, return NULL.
 */
struct matrix *add_matrices(struct matrix *A, struct matrix *B, char sign)
{
    if (A->rows != B->rows || A->cols != B->cols)
    {
        return NULL;
    }

    struct matrix *result = gen_matrix(A->rows, A->cols);
    for (int row = 0; row < A->rows; row++)
    {
        for (int col = 0; col < B->cols; col++)
        {
            int *p_rel = result->vals + row * A->cols + col; // result element
            if (sign == '-')
                *p_rel = *(A->vals + row * A->cols + col) - *(B->vals + row * B->cols + col);
            else if (sign == '+')
                *p_rel = *(A->vals + row * A->cols + col) + *(B->vals + row * B->cols + col);
        }
    }
    return result;
}

/**
 * Get a transposed copy of the passed matrix.
 */
struct matrix *transpose(struct matrix *A)
{
    struct matrix *result = gen_matrix(A->cols, A->rows);
    for (int row = 0; row < A->rows; row++)
    {
        for (int col = 0; col < A->cols; col++)
        {
            int *p_mel = A->vals + row * A->cols + col; // matrix element
            int *p_rel = result->vals + col * A->rows + row;
            *p_rel = *p_mel;
        }
    }
    return result;
}

/*
 * Fill the matrix with random integers.
 */
void randomize_matrix(struct matrix *A)
{
    // Set the received matrix with random ints
    for (int row = 0; row < A->rows; row++)
    {
        for (int col = 0; col < A->cols; col++)
        {
            int *p_el = A->vals + row * A->cols + col; // pointer on a matrix element
            *p_el = rand() % 5 + 1;                    // new value
        }
    }
}

/**
 * Print the matrix.
 */
void print_matrix(struct matrix *A)
{
    // Display matrix
    for (int row = 0; row < A->rows; row++)
    {
        for (int col = 0; col < A->cols; col++)
        {
            printf("%d\t", *(A->vals + row * A->cols + col));
        }
        printf("\n");
    }
}

/*
 * Delete a row by its index from the matrix.
 * If the row index is out of range, do nothing.
 */
void del_row(struct matrix *A, int krow)
{
    if (krow > 0 && krow <= A->rows)
    {
        krow--;
    }
    else
    {
        printf("Номер ряда в диапазоне: 1..%d\n", A->rows);
        return;
    }

    int jump = 0; // predicate for skipping a row
    // it could be used in subtraction for manipulation with rows
    int *new_array = calloc((A->rows - 1) * A->cols, sizeof(int *));
    for (int row = 0; row < A->rows; row++)
    {
        for (int col = 0; col < A->cols; col++)
        {
            if (row != krow)
            {
                if (jump == 0)
                {
                    int *p_rel = new_array + row * A->cols + col;
                    *p_rel = *(A->vals + row * A->cols + col);
                }
                else if (jump > 0)
                {
                    int *p_rel = new_array + (row - jump) * A->cols + col;
                    *p_rel = *(A->vals + row * A->cols + col);
                }
            }
            else
            {
                jump++;
                col = A->cols;
            }
        }
    }
    free(A->vals);
    A->vals = new_array;
    A->rows--;
    A->length = A->rows * A->cols;
}

/**
 * Allocate matrix.
 * If the passed dimensions are invalid, return NULL.
 */
struct matrix *gen_matrix(int rows, int cols)
{
    // Generate matrix, values are undefined
    if (rows < 0 || cols < 0)
    {
        return NULL;
    }

    struct matrix *result = malloc(sizeof(struct matrix));

    result->rows = rows;
    result->cols = cols;
    result->length = result->rows * result->cols;
    result->vals = calloc(result->length, sizeof(int));

    return result;
}

/*
 * Free the memory allocated bu the matrix.
 */
void free_matrix(struct matrix *A)
{
    free(A->vals);
    free(A);
}
