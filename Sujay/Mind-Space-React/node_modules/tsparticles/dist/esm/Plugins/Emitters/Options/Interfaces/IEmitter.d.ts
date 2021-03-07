import type { ICoordinates } from "../../../../Core/Interfaces/ICoordinates";
import type { MoveDirection, MoveDirectionAlt } from "../../../../Enums";
import type { IParticles } from "../../../../Options/Interfaces/Particles/IParticles";
import type { IEmitterRate } from "./IEmitterRate";
import type { IEmitterLife } from "./IEmitterLife";
import type { RecursivePartial } from "../../../../Types";
import type { IEmitterSize } from "./IEmitterSize";
export interface IEmitter {
    size?: IEmitterSize;
    direction: MoveDirection | keyof typeof MoveDirection | MoveDirectionAlt;
    life: IEmitterLife;
    particles?: RecursivePartial<IParticles>;
    position?: RecursivePartial<ICoordinates>;
    rate: IEmitterRate;
}
