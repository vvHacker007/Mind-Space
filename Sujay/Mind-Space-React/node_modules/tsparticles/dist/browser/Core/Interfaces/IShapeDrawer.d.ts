import type { ShapeDrawerAfterEffectFunction, ShapeDrawerDestroyFunction, ShapeDrawerDrawFunction, ShapeDrawerInitFunction, ShapeDrawerSidesCountFunction } from "../../Types";
export interface IShapeDrawer {
    getSidesCount?: ShapeDrawerSidesCountFunction;
    init?: ShapeDrawerInitFunction;
    draw: ShapeDrawerDrawFunction;
    afterEffect?: ShapeDrawerAfterEffectFunction;
    destroy?: ShapeDrawerDestroyFunction;
}
