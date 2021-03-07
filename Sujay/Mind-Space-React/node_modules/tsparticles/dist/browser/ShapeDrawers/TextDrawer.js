var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { Utils } from "../Utils";
import { ShapeType } from "../Enums";
export class TextDrawer {
    getSidesCount() {
        return 12;
    }
    init(container) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            const options = container.options;
            if (Utils.isInArray(ShapeType.char, options.particles.shape.type) ||
                Utils.isInArray(ShapeType.character, options.particles.shape.type)) {
                const shapeOptions = ((_a = options.particles.shape.options[ShapeType.character]) !== null && _a !== void 0 ? _a : options.particles.shape.options[ShapeType.char]);
                if (shapeOptions instanceof Array) {
                    for (const character of shapeOptions) {
                        yield Utils.loadFont(character);
                    }
                }
                else {
                    if (shapeOptions !== undefined) {
                        yield Utils.loadFont(shapeOptions);
                    }
                }
            }
        });
    }
    draw(context, particle, radius) {
        const character = particle.shapeData;
        if (character === undefined) {
            return;
        }
        const textData = character.value;
        if (textData === undefined) {
            return;
        }
        const textParticle = particle;
        if (textParticle.text === undefined) {
            textParticle.text =
                textData instanceof Array ? Utils.itemFromArray(textData, particle.randomIndexData) : textData;
        }
        const text = textParticle.text;
        const style = character.style;
        const weight = character.weight;
        const size = Math.round(radius) * 2;
        const font = character.font;
        const fill = particle.fill;
        const offsetX = (text.length * radius) / 2;
        context.font = `${style} ${weight} ${size}px "${font}"`;
        const pos = {
            x: -offsetX,
            y: radius / 2,
        };
        if (fill) {
            context.fillText(text, pos.x, pos.y);
        }
        else {
            context.strokeText(text, pos.x, pos.y);
        }
    }
}
