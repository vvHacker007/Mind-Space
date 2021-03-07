import type { ISizeAnimation } from "../../../Interfaces/Particles/Size/ISizeAnimation";
import type { RecursivePartial } from "../../../../Types";
import { DestroyType, StartValueType } from "../../../../Enums";
import type { IOptionLoader } from "../../../Interfaces/IOptionLoader";
export declare class SizeAnimation implements ISizeAnimation, IOptionLoader<ISizeAnimation> {
    get size_min(): number;
    set size_min(value: number);
    destroy: DestroyType | keyof typeof DestroyType;
    enable: boolean;
    minimumValue: number;
    speed: number;
    startValue: StartValueType | keyof typeof StartValueType;
    sync: boolean;
    constructor();
    load(data?: RecursivePartial<ISizeAnimation>): void;
}
