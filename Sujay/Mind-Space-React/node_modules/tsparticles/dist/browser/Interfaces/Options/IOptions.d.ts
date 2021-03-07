import type { IOptions as ICoreOptions } from "../../Options/Interfaces/IOptions";
import type { IPolygonMaskOptions } from "../../Plugins/PolygonMask/PolygonMaskPlugin";
import type { IEmitterOptions } from "../../Plugins/Emitters/EmittersPlugin";
import type { IAbsorberOptions } from "../../Plugins/Absorbers/AbsorbersPlugin";
export declare type IOptions = ICoreOptions & IAbsorberOptions & IEmitterOptions & IPolygonMaskOptions;
