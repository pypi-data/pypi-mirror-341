#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "load_inst.hpp"
#include "freq_miner.hpp"
#include "utility.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
    m.doc() = "Efficient Sequential Pattern Mining via Prefix-Projection";

    m.def("mine", [](std::string data_file, double minsup) {
        ClearCollected();

        // Note: Pass by value (safe copy)
        if (!Load_instance(data_file, minsup)) {
            throw std::runtime_error("Failed to load database from " + data_file);
        }

        Freq_miner();
        return GetCollected();
    },
    py::arg("data_file"),
    py::arg("minsup") = 0.01,
    "Mine sequential patterns from the given data file with minimum support.");
}
