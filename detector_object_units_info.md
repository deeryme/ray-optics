# Detector object units info
- P: The rate of energy flow (flux) in B/s (see below).
- F⊥: The rate of perpendicular momentum flow in (B/s)/c.
- F∥: The rate of parallel momentum flow in (B/s)/c.
- The irradiance in the exported CSV is in (B/s)/L.
- L is the arbitrary unit of length used in this simulator.
- B is an arbitrary unit of radiant flux or luminous flux, corresponding to the unit of the "Brightness" option being B/L for non-Lambertian beams and 500B/360° for point sources.
- The dimensionless factor s is the "Brightness Scale" shown in Settings -> Show status box, which equals 1 when "Ray Density" is above some threshold and proportional to "Ray Density" otherwise.
- If some rays are truncated in the infinite series of internal reflection, the total truncation is shown as error estimates.