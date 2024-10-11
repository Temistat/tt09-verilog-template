# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.a.value = 13
    dut.b.value = 10

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 10)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    dut._log.info(f"value of outputs are: {dut.sum.value} and {dut.carry_out.value}.")
    assert dut.sum.value == 7 and dut.carry_out.value == 1 

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
    import cocotb
from cocotb.triggers import RisingEdge
import random

@cocotb.test()
async def test_koggestone_adder_4bit(dut):
    """Test Kogge-Stone Adder 4-bit with corner cases and random inputs"""
    
    # Edge case tests
    test_cases = [
        (0b0000, 0b0000, 0b0000, 0),  # 0 + 0 = 0
        (0b0101, 0b0011, 0b1000, 0),  # 5 + 3 = 8
        (0b1111, 0b0001, 0b0000, 1),  # 15 + 1 = 16 (carry out = 1)
        (0b1100, 0b0011, 0b1111, 0),  # 12 + 3 = 15
    ]

    for a, b, expected_sum, expected_carry in test_cases:
        dut.ui_in <= (b << 4) | a  # Concatenate inputs a and b
        dut.ena <= 1
        dut.rst_n <= 1
        await RisingEdge(dut.clk)
        
        assert dut.sum.value == expected_sum, f"sum mismatch: {dut.sum.value} != {expected_sum}"
        assert dut.carry_out.value == expected_carry, f"carry mismatch: {dut.carry_out.value} != {expected_carry}"

    # Randomized tests for 1000 cases
    for _ in range(1000):
        a = random.randint(0, 15)  # Random 4-bit input
        b = random.randint(0, 15)
        expected_sum = (a + b) % 16
        expected_carry = (a + b) // 16

        dut.ui_in <= (b << 4) | a
        dut.ena <= 1
        dut.rst_n <= 1
        await RisingEdge(dut.clk)

        assert dut.sum.value == expected_sum, f"sum mismatch: {dut.sum.value} != {expected_sum}"
        assert dut.carry_out.value == expected_carry, f"carry mismatch: {dut.carry_out.value} != {expected_carry}"

    
