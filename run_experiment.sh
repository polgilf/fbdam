# From the repository root
for scenario in \
  scenarios/ds-a_alpha-0.4.yaml \
  scenarios/ds-a_alpha-0.6.yaml \
  scenarios/ds-b_alpha-0.4.yaml \
  scenarios/ds-b_alpha-0.6.yaml
  do
    python -m fbdam.engine.run run "$scenario" --profile time-limited
    python -m fbdam.engine.run run "$scenario" --profile gap-limited
  done