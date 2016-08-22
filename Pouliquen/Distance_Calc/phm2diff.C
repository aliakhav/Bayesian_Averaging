/*
 * phm_area.cpp
 *
 *  Created on: Jul 4, 2016
 *      Author: ali
 */

#include <stdio.h>
#include <stdlib.h>

int main() {

	int NS, N;
	N = 256;
	double DI[N][2];

	for (NS = 0; NS < N; NS++)
	{
		char filename[50];
		sprintf(filename, "pileheightrecord%d", NS);

		FILE* phm = fopen(filename, "r");

		if (!phm) {
			perror("File opening failed");
			return EXIT_FAILURE;
		}

		int Nx, Ny;
		float x_range[2], y_range[2];

		fscanf(phm, "Nx=%d: X= {%g,%g}\nNy=%d: Y= {%g,%g", &Nx, &x_range[0],
				&x_range[1], &Ny, &y_range[0], &y_range[1]);

		double dx = (x_range[1] - x_range[0]) / Nx;
		double dy = (y_range[1] - y_range[0]) / Ny;

		char blank[100];
		fgets(blank, 100, phm);
		fgets(blank, 100, phm);

		float** h_value = new float*[Ny];
		for (int i = 0; i < Ny; ++i)
			h_value[i] = new float[Nx];

		int iy, ix;
		for (iy = 0; iy < Ny; iy++) {
			for (ix = 0; ix < Nx - 1; ix++)
				fscanf(phm, "%g ", &h_value[iy][ix]);
			fscanf(phm, "%g\n", &h_value[iy][ix]);
		}

		fclose(phm);



		int** YX = new int*[1730];
		for (int i = 0; i < 1730; i++)
			YX[i] = new int[2];

		int nn = 0;

		FILE* xdata1 = fopen("XX1.csv", "r");

		for (iy = 0; iy < 44; iy++) {
			fscanf(xdata1, "%d %d\n", &YX[nn][0], &YX[nn + 1][0]);

			nn += 2;
		}

		fclose(xdata1);

		FILE* xdata2 = fopen("XX2.csv", "r");

		for (iy = 0; iy < 238; iy++) {
			fscanf(xdata2, "%d %d %d %d\n", &YX[nn][0], &YX[nn + 1][0],
					&YX[nn + 2][0], &YX[nn + 3][0]);

			nn += 4;
		}

		fclose(xdata2);

		FILE* xdata3 = fopen("XX3.csv", "r");

		for (iy = 0; iy < 115; iy++) {
			fscanf(xdata3, "%d %d %d %d %d %d\n", &YX[nn][0], &YX[nn + 1][0],
					&YX[nn + 2][0], &YX[nn + 3][0], &YX[nn + 4][0], &YX[nn + 5][0]);

			nn += 6;
		}

		fclose(xdata3);
	////////////////////////////////////////////
		FILE* ydata = fopen("YY.csv", "r");
		nn = 0;

		for (iy = 0; iy < 44; iy++) {
			fscanf(ydata, "%d\n", &YX[nn][1]);
			YX[nn + 1][1] = YX[nn][1];
			nn += 2;
		}

		for (iy = 0; iy < 238; iy++) {
			fscanf(ydata, "%d\n", &YX[nn][1]);
			YX[nn + 1][1] = YX[nn][1];
			YX[nn + 2][1] = YX[nn][1];
			YX[nn + 3][1] = YX[nn][1];
			nn += 4;
		}

		for (iy = 0; iy < 115; iy++) {
			fscanf(ydata, "%d\n", &YX[nn][1]);
			YX[nn + 1][1] = YX[nn][1];
			YX[nn + 2][1] = YX[nn][1];
			YX[nn + 3][1] = YX[nn][1];
			YX[nn + 4][1] = YX[nn][1];
			YX[nn + 5][1] = YX[nn][1];
			nn += 6;
		}

		fclose(ydata);
	////////////////////////////////////////////
		for (int i = 0; i < 1730; ++i)
			for (int j = 0; j < 2; ++j)
				YX[i][j] += 1;

		double** fieldD = new double*[Ny];
		for (int i = 0; i < Ny; ++i)
			fieldD[i] = new double[Nx];

		for (int i = 0; i < Ny; ++i)
			for (int j = 0; j < Nx; ++j)
				fieldD[i][j] = 0.0;

		int k;

		for (int i = 0; i < 865; i++) {
			k = YX[2 * i][1];
			for (int j = YX[2 * i][0]; j < YX[2 * i + 1][0] + 1; j++)
				fieldD[k][j] = 2.0;
		}

		fieldD[1608][1597] = 2.0;
		fieldD[1210][1179] = 2.0;

		double threshold = 0.1;


			double count_s = 0;
			for (iy = 0; iy < Ny; iy++) {
				for (ix = 0; ix < Nx; ix++) {
					if (h_value[iy][ix] > 0.0) {
						if (h_value[iy][ix] > threshold) {
							count_s += 1;
							h_value[iy][ix] = 3.0;
						} else
							h_value[iy][ix] = 0.0;
					}
				}
			}

			double cell_Ar = dx * dy;

			double count_fd = 0;
			double symm_diff = 0.0;
			double intersect = 0.0;

			for (iy = 0; iy < Ny; iy++)
				for (ix = 0; ix < Nx; ix++) {
					h_value[iy][ix] += fieldD[iy][ix];

					if (fieldD[iy][ix] > 0.0)
						count_fd += 1;

					if (h_value[iy][ix] == 5.0)
						intersect += 1.0;

					if (h_value[iy][ix] == 2.0 || h_value[iy][ix] == 3.0)
						symm_diff += 1.0;
				}

		count_s *= cell_Ar;
		count_fd *= cell_Ar;
		symm_diff *= cell_Ar;
		intersect *= cell_Ar;

		DI[NS][0] = symm_diff/count_fd;
		DI[NS][1] = intersect/count_fd;

		printf("%f,%f,%f\n", DI[NS][0], DI[NS][1], DI[NS][0]/DI[NS][1]);

////////////////////////////////////////////////
		for (int i = 0; i < Ny; ++i)
			delete[] h_value[i];
		delete[] h_value;

		for (int i = 0; i < Ny; ++i)
			delete[] fieldD[i];
		delete[] fieldD;

		for (int i = 0; i < 1730; ++i)
			delete[] YX[i];
		delete[] YX;
	}

	FILE* DF = fopen("Diff_P.csv", "w");
	for (int ii = 0; ii < N; ii++)
		fprintf(DF,"%f,%f,%f\n", DI[ii][0], DI[ii][1], DI[ii][0]/DI[ii][1]);

	fclose(DF);

	return 0;
}

