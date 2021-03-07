import type { AnimationStatus } from "../../Enums";
export interface IParticleValueAnimation<T> {
    status?: AnimationStatus;
    velocity?: number;
    value: T;
}
