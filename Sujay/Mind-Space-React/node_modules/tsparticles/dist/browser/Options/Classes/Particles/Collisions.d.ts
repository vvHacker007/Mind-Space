import type { ICollisions } from "../../Interfaces/Particles/ICollisions";
import { CollisionMode } from "../../../Enums";
import type { RecursivePartial } from "../../../Types";
import type { IOptionLoader } from "../../Interfaces/IOptionLoader";
import { Bounce } from "./Bounce/Bounce";
export declare class Collisions implements ICollisions, IOptionLoader<ICollisions> {
    bounce: Bounce;
    enable: boolean;
    mode: CollisionMode | keyof typeof CollisionMode;
    constructor();
    load(data?: RecursivePartial<ICollisions>): void;
}
