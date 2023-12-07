#ifndef ERODR_H
#define ERODR_H

#ifdef __cplusplus
extern "C" {
#endif

void simulate_particles(double *hmap, int width, int height, int n, int ttl, double p_enertia, double p_min_slope, double p_capacity, double p_deposition, double p_erosion, int p_radius, double p_gravity, double p_evaporation);

#ifdef __cplusplus
}
#endif

#endif
