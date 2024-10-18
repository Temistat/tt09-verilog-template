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

    # 1000 random tests
    for i in range(1000):
        # Generate two random 4-bit numbers
        a = random.randint(0, 15)
        b = random.randint(0, 15)

        # Set input values to the device under test (DUT)
        dut.a.value = a
        dut.b.value = b

        # Wait for one or more clock cycles to process the inputs
        await ClockCycles(dut.clk, 10)

        # Compute the expected sum and carry-out using Python's built-in addition
        expected_sum = (a + b) % 16  # Mod 16 to stay within 4 bits
        expected_carry_out = (a + b) // 16  # Carry-out is 1 if the result is > 15

        # Log the inputs and outputs for traceability
        dut._log.info(f"Test {i + 1}: a={a}, b={b}, expected_sum={expected_sum}, expected_carry={expected_carry_out}")

        # Assert that the DUT produces the correct sum and carry-out
        assert dut.sum.value == expected_sum, f"Test {i + 1} failed: sum={dut.sum.value} != expected_sum={expected_sum}"
        assert dut.carry_out.value == expected_carry_out, f"Test {i + 1} failed: carry_out={dut.carry_out.value} != expected_carry_out={expected_carry_out}"

    dut._log.info("All 1000 tests passed!")