import type { IOpacityAnimation } from "../../../Interfaces/Particles/Opacity/IOpacityAnimation";
import type { RecursivePartial } from "../../../../Types";
import type { IOptionLoader } from "../../../Interfaces/IOptionLoader";
import { DestroyType, StartValueType } from "../../../../Enums/Types";
export declare class OpacityAnimation implements IOpacityAnimation, IOptionLoader<IOpacityAnimation> {
    get opacity_min(): number;
    set opacity_min(value: number);
    destroy: DestroyType | keyof typeof DestroyType;
    enable: boolean;
    minimumValue: number;
    speed: number;
    startValue: StartValueType | keyof typeof StartValueType;
    sync: boolean;
    constructor();
    load(data?: RecursivePartial<IOpacityAnimation>): void;
}
