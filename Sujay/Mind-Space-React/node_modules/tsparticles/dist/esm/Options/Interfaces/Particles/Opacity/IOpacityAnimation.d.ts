import { DestroyType, StartValueType } from "../../../../Enums/Types";
export interface IOpacityAnimation {
    opacity_min: number;
    destroy: DestroyType | keyof typeof DestroyType;
    enable: boolean;
    minimumValue: number;
    speed: number;
    sync: boolean;
    startValue: StartValueType | keyof typeof StartValueType;
}
