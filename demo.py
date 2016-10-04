import picosat

with open("/tmp/log", "w") as fout:
    p = picosat.picosat_init()
    picosat.picosat_set_verbosity(p, 100)
    f = picosat.picosat_set_output(p, fout)
    picosat.picosat_measure_all_calls(p)
    picosat.picosat_inc_max_var(p)
    picosat.picosat_add(p, 1)
    picosat.picosat_add(p, -1)
    picosat.picosat_add(p, 0)
    assert picosat.picosat_sat(p, -1) == picosat.PICOSAT_SATISFIABLE
    picosat.picosat_message(p, 0, "End")
    picosat.picosat_flushout(f)
    picosat.picosat_reset(p)
print("Done.")
