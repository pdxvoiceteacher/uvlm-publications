# Methods Appendix

## Synthetic controls

The WAVE Gold-Physics family uses closed-form waveform metric calibration. It varies phase, frequency, amplitude, noise, and jitter in synthetic traces with known expected behavior.

## Core equations

```text
x1(t) = A1 sin(2πf1t + φ1)
x2(t) = A2 sin(2πf2t + φ2)
y(t) = x1(t) + x2(t)
Δφ = φ2 − φ1
interference_polarity = cos(Δφ)
constructive_potential = Ψ × (1 + cos Δφ) / 2
cancellation_risk = Ψ × (1 − cos Δφ) / 2
residual_peak_amplitude ≈ |A1 − A2|
residual_rms ≈ |A1 − A2| / sqrt(2)
d(Δφ)/dt = 2π(f2 − f1)
```

## Interpretation rules

- Constructive phase can increase output amplitude.
- Anti-phase can cancel output even at high Ψ.
- Quadrature separates constructive and destructive extremes.
- Detuning produces recurrent rephasing and beat events.
- Unequal amplitudes produce incomplete cancellation residuals.
- Noise and jitter degrade observability and may raise ΔS without proving structural incoherence.
- Eₛ is not applicable for synthetic waveform physics unless agentic, social, deployment, or human-impact domains are introduced.

This appendix is not truth certification, not deployment authority, and not final answer authority.
