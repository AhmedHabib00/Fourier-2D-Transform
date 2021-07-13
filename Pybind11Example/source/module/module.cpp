#include <complex>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include<pybind11/complex.h>
using namespace std;
#define M_PI   3.14159265358979323846264338327950288
namespace py = pybind11;
vector<complex<double>> dft(vector<complex<double>> X)
{
	//determine number of samples
	int N = X.size();
	int K = N;

	//allocate memery for output
	complex<double> intSum;

	//allocate memory for output
	vector<complex<double>> output;
	output.reserve(K);

	//loop through each k
	for (int k = 0; k < K; k++)
	{
		//loop through each n
		intSum = complex<double>(0, 0);
		for (int n = 0; n < N; n++)
		{
			double realPart = cos(((2 * M_PI) / N) * k * n);
			double imagPart = sin(((2 * M_PI) / N) * k * n);
			complex <double> w(realPart, -imagPart);
			intSum += X[n] * w;
		}
		output.push_back(intSum);
	}
	return output;
}
vector<complex<double>> FFT(vector<complex<double>>& sampels)
{
	int N = sampels.size();
	if (N == 1)
	{
		return sampels;
	}

	int K = N / 2;

	vector<complex<double>> Even(K, 0);
	vector<complex<double>> Odd(K, 0);
	int z = 0;
	int y = 0;
	for (int i = 0; i != K; i++)
	{
		Even[i] = sampels[2 * i];
		Odd[i] = sampels[2 * i + 1];
	}
	vector<complex<double>> FinEven(K, 0);
	vector<complex<double>> FinOdd(K, 0);
	FinEven = FFT(Even);
	FinOdd = FFT(Odd);
	vector<complex<double>> Frequencies(N, 0);
	for (int k = 0; k != N / 2; k++)
	{
		complex<double>t = polar(1.0, -2 * M_PI * k / N) * FinOdd[k];
		Frequencies[k] = FinEven[k] + t;
		Frequencies[k + K] = FinEven[k] - t;
	}
	return Frequencies;
}

PYBIND11_MODULE(pybind11module, module)
{
	module.def("dft", &dft);
	module.def("FFT", &FFT);
}