import type { DestroyType, StartValueType } from "../../../../Enums";
export interface ISizeAnimation {
    size_min: number;
    destroy: DestroyType | keyof typeof DestroyType;
    enable: boolean;
    minimumValue: number;
    speed: number;
    sync: boolean;
    startValue: StartValueType | keyof typeof StartValueType;
}
