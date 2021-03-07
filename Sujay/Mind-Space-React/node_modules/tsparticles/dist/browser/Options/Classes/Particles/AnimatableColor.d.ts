import type { IAnimatableColor } from "../../Interfaces/Particles/IAnimatableColor";
import { OptionsColor } from "../OptionsColor";
import type { RecursivePartial } from "../../../Types";
import { ColorAnimation } from "./ColorAnimation";
import type { IOptionLoader } from "../../Interfaces/IOptionLoader";
export declare class AnimatableColor extends OptionsColor implements IAnimatableColor, IOptionLoader<IAnimatableColor> {
    animation: ColorAnimation;
    constructor();
    static create(source?: AnimatableColor, data?: string | RecursivePartial<IAnimatableColor>): AnimatableColor;
    load(data?: RecursivePartial<IAnimatableColor>): void;
}
