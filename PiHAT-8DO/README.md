**2. WIN-PiHAT-8DO(Relay).py**
A sequential diagnostic script that cycles through the 8 electromechanical relays one by one. It drives the corresponding GPIO pins HIGH for one second each, providing audible (clicks) and visual (LEDs) confirmation that the relay coils and output stages are functioning correctly.

**3. WIN-PiHAT-8DO(MOSFET).py**
A rapid-switching test utility designed for the solid-state output board. It systematically pulses each of the 8 MOSFET channels, verifying the Pi's GPIO mapping and the high-side load switching capabilities without the mechanical wear associated with relay testing.
