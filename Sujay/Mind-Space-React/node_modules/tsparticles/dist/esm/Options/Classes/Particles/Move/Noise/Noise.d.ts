import type { INoise } from "../../../../Interfaces/Particles/Move/Noise/INoise";
import type { RecursivePartial } from "../../../../../Types";
import { NoiseDelay } from "./NoiseDelay";
import type { IOptionLoader } from "../../../../Interfaces/IOptionLoader";
export declare class Noise implements INoise, IOptionLoader<INoise> {
    delay: NoiseDelay;
    enable: boolean;
    constructor();
    load(data?: RecursivePartial<INoise>): void;
}
