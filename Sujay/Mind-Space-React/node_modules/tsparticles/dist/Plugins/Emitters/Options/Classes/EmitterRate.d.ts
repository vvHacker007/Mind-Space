import type { IEmitterRate } from "../Interfaces/IEmitterRate";
import type { RecursivePartial } from "../../../../Types";
import type { IOptionLoader } from "../../../../Options/Interfaces/IOptionLoader";
export declare class EmitterRate implements IEmitterRate, IOptionLoader<IEmitterRate> {
    quantity: number;
    delay: number;
    constructor();
    load(data?: RecursivePartial<IEmitterRate>): void;
}
