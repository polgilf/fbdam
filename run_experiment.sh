# From the repository root
for scenario in \
  scenarios/ds-a_dials-balanced.yaml \
  scenarios/ds-a_dials-efficiency.yaml \
  scenarios/ds-a_dials-fairness.yaml \
  scenarios/ds-a_dials-adequacy.yaml \
  scenarios/ds-a_dials-fairness-adequacy.yaml \
  scenarios/ds-a_dials-hard-fairness.yaml \
  #scenarios/ds-b_dials-balanced.yaml \
  #scenarios/ds-b_dials-efficiency.yaml \
  #scenarios/ds-b_dials-fairness.yaml \
  #scenarios/ds-b_dials-hard-fairness.yaml \
  do
    python -m fbdam.engine.run run "$scenario" --profile time-limited
    # python -m fbdam.engine.run run "$scenario" --profile gap-limited
  done