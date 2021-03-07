import { ColorUtils } from "./ColorUtils";
import { NumberUtils } from "./NumberUtils";
function drawLine(context, begin, end) {
    context.beginPath();
    context.moveTo(begin.x, begin.y);
    context.lineTo(end.x, end.y);
    context.closePath();
}
function drawTriangle(context, p1, p2, p3) {
    context.beginPath();
    context.moveTo(p1.x, p1.y);
    context.lineTo(p2.x, p2.y);
    context.lineTo(p3.x, p3.y);
    context.closePath();
}
export class CanvasUtils {
    static paintBase(context, dimension, baseColor) {
        context.save();
        context.fillStyle = baseColor !== null && baseColor !== void 0 ? baseColor : "rgba(0,0,0,0)";
        context.fillRect(0, 0, dimension.width, dimension.height);
        context.restore();
    }
    static clear(context, dimension) {
        context.clearRect(0, 0, dimension.width, dimension.height);
    }
    static drawLinkLine(context, width, begin, end, maxDistance, canvasSize, warp, backgroundMask, composite, colorLine, opacity, shadow) {
        let drawn = false;
        if (NumberUtils.getDistance(begin, end) <= maxDistance) {
            drawLine(context, begin, end);
            drawn = true;
        }
        else if (warp) {
            let pi1;
            let pi2;
            const endNE = {
                x: end.x - canvasSize.width,
                y: end.y,
            };
            const d1 = NumberUtils.getDistances(begin, endNE);
            if (d1.distance <= maxDistance) {
                const yi = begin.y - (d1.dy / d1.dx) * begin.x;
                pi1 = { x: 0, y: yi };
                pi2 = { x: canvasSize.width, y: yi };
            }
            else {
                const endSW = {
                    x: end.x,
                    y: end.y - canvasSize.height,
                };
                const d2 = NumberUtils.getDistances(begin, endSW);
                if (d2.distance <= maxDistance) {
                    const yi = begin.y - (d2.dy / d2.dx) * begin.x;
                    const xi = -yi / (d2.dy / d2.dx);
                    pi1 = { x: xi, y: 0 };
                    pi2 = { x: xi, y: canvasSize.height };
                }
                else {
                    const endSE = {
                        x: end.x - canvasSize.width,
                        y: end.y - canvasSize.height,
                    };
                    const d3 = NumberUtils.getDistances(begin, endSE);
                    if (d3.distance <= maxDistance) {
                        const yi = begin.y - (d3.dy / d3.dx) * begin.x;
                        const xi = -yi / (d3.dy / d3.dx);
                        pi1 = { x: xi, y: yi };
                        pi2 = { x: pi1.x + canvasSize.width, y: pi1.y + canvasSize.height };
                    }
                }
            }
            if (pi1 && pi2) {
                drawLine(context, begin, pi1);
                drawLine(context, end, pi2);
                drawn = true;
            }
        }
        if (!drawn) {
            return;
        }
        context.lineWidth = width;
        if (backgroundMask) {
            context.globalCompositeOperation = composite;
        }
        context.strokeStyle = ColorUtils.getStyleFromRgb(colorLine, opacity);
        if (shadow.enable) {
            const shadowColor = ColorUtils.colorToRgb(shadow.color);
            if (shadowColor) {
                context.shadowBlur = shadow.blur;
                context.shadowColor = ColorUtils.getStyleFromRgb(shadowColor);
            }
        }
        context.stroke();
    }
    static drawLinkTriangle(context, pos1, pos2, pos3, backgroundMask, composite, colorTriangle, opacityTriangle) {
        drawTriangle(context, pos1, pos2, pos3);
        if (backgroundMask) {
            context.globalCompositeOperation = composite;
        }
        context.fillStyle = ColorUtils.getStyleFromRgb(colorTriangle, opacityTriangle);
        context.fill();
    }
    static drawConnectLine(context, width, lineStyle, begin, end) {
        context.save();
        drawLine(context, begin, end);
        context.lineWidth = width;
        context.strokeStyle = lineStyle;
        context.stroke();
        context.restore();
    }
    static gradient(context, p1, p2, opacity) {
        const gradStop = Math.floor(p2.getRadius() / p1.getRadius());
        const color1 = p1.getFillColor();
        const color2 = p2.getFillColor();
        if (!color1 || !color2) {
            return;
        }
        const sourcePos = p1.getPosition();
        const destPos = p2.getPosition();
        const midRgb = ColorUtils.mix(color1, color2, p1.getRadius(), p2.getRadius());
        const grad = context.createLinearGradient(sourcePos.x, sourcePos.y, destPos.x, destPos.y);
        grad.addColorStop(0, ColorUtils.getStyleFromHsl(color1, opacity));
        grad.addColorStop(gradStop > 1 ? 1 : gradStop, ColorUtils.getStyleFromRgb(midRgb, opacity));
        grad.addColorStop(1, ColorUtils.getStyleFromHsl(color2, opacity));
        return grad;
    }
    static drawGrabLine(context, width, begin, end, colorLine, opacity) {
        context.save();
        drawLine(context, begin, end);
        context.strokeStyle = ColorUtils.getStyleFromRgb(colorLine, opacity);
        context.lineWidth = width;
        context.stroke();
        context.restore();
    }
    static drawLight(container, context, mousePos) {
        const lightOptions = container.options.interactivity.modes.light.area;
        context.beginPath();
        context.arc(mousePos.x, mousePos.y, lightOptions.radius, 0, 2 * Math.PI);
        const gradientAmbientLight = context.createRadialGradient(mousePos.x, mousePos.y, 0, mousePos.x, mousePos.y, lightOptions.radius);
        const gradient = lightOptions.gradient;
        const gradientRgb = {
            start: ColorUtils.colorToRgb(gradient.start),
            stop: ColorUtils.colorToRgb(gradient.stop),
        };
        if (!gradientRgb.start || !gradientRgb.stop) {
            return;
        }
        gradientAmbientLight.addColorStop(0, ColorUtils.getStyleFromRgb(gradientRgb.start));
        gradientAmbientLight.addColorStop(1, ColorUtils.getStyleFromRgb(gradientRgb.stop));
        context.fillStyle = gradientAmbientLight;
        context.fill();
    }
    static drawParticleShadow(container, context, particle, mousePos) {
        const pos = particle.getPosition();
        const shadowOptions = container.options.interactivity.modes.light.shadow;
        context.save();
        const radius = particle.getRadius();
        const sides = particle.sides;
        const full = (Math.PI * 2) / sides;
        const angle = -particle.rotate.value + Math.PI / 4;
        const factor = 1;
        const dots = [];
        for (let i = 0; i < sides; i++) {
            dots.push({
                x: pos.x + radius * Math.sin(angle + full * i) * factor,
                y: pos.y + radius * Math.cos(angle + full * i) * factor,
            });
        }
        const points = [];
        const shadowLength = shadowOptions.length;
        for (const dot of dots) {
            const dotAngle = Math.atan2(mousePos.y - dot.y, mousePos.x - dot.x);
            const endX = dot.x + shadowLength * Math.sin(-dotAngle - Math.PI / 2);
            const endY = dot.y + shadowLength * Math.cos(-dotAngle - Math.PI / 2);
            points.push({
                endX: endX,
                endY: endY,
                startX: dot.x,
                startY: dot.y,
            });
        }
        const shadowRgb = ColorUtils.colorToRgb(shadowOptions.color);
        if (!shadowRgb) {
            return;
        }
        const shadowColor = ColorUtils.getStyleFromRgb(shadowRgb);
        for (let i = points.length - 1; i >= 0; i--) {
            const n = i == points.length - 1 ? 0 : i + 1;
            context.beginPath();
            context.moveTo(points[i].startX, points[i].startY);
            context.lineTo(points[n].startX, points[n].startY);
            context.lineTo(points[n].endX, points[n].endY);
            context.lineTo(points[i].endX, points[i].endY);
            context.fillStyle = shadowColor;
            context.fill();
        }
        context.restore();
    }
    static drawParticle(container, context, particle, delta, fillColorValue, strokeColorValue, backgroundMask, composite, radius, opacity, shadow) {
        const pos = particle.getPosition();
        context.save();
        context.translate(pos.x, pos.y);
        context.beginPath();
        const angle = particle.rotate.value + (particle.particlesOptions.rotate.path ? particle.pathAngle : 0);
        if (angle !== 0) {
            context.rotate(angle);
        }
        if (backgroundMask) {
            context.globalCompositeOperation = composite;
        }
        const shadowColor = particle.shadowColor;
        if (shadow.enable && shadowColor) {
            context.shadowBlur = shadow.blur;
            context.shadowColor = ColorUtils.getStyleFromRgb(shadowColor);
            context.shadowOffsetX = shadow.offset.x;
            context.shadowOffsetY = shadow.offset.y;
        }
        if (fillColorValue) {
            context.fillStyle = fillColorValue;
        }
        const stroke = particle.stroke;
        context.lineWidth = particle.strokeWidth;
        if (strokeColorValue) {
            context.strokeStyle = strokeColorValue;
        }
        CanvasUtils.drawShape(container, context, particle, radius, opacity, delta);
        if (stroke.width > 0) {
            context.stroke();
        }
        if (particle.close) {
            context.closePath();
        }
        if (particle.fill) {
            context.fill();
        }
        context.restore();
        context.save();
        context.translate(pos.x, pos.y);
        if (angle !== 0) {
            context.rotate(angle);
        }
        if (backgroundMask) {
            context.globalCompositeOperation = composite;
        }
        CanvasUtils.drawShapeAfterEffect(container, context, particle, radius, opacity, delta);
        context.restore();
    }
    static drawShape(container, context, particle, radius, opacity, delta) {
        if (!particle.shape) {
            return;
        }
        const drawer = container.drawers.get(particle.shape);
        if (!drawer) {
            return;
        }
        drawer.draw(context, particle, radius, opacity, delta.value, container.retina.pixelRatio);
    }
    static drawShapeAfterEffect(container, context, particle, radius, opacity, delta) {
        if (!particle.shape) {
            return;
        }
        const drawer = container.drawers.get(particle.shape);
        if (!(drawer === null || drawer === void 0 ? void 0 : drawer.afterEffect)) {
            return;
        }
        drawer.afterEffect(context, particle, radius, opacity, delta.value, container.retina.pixelRatio);
    }
    static drawPlugin(context, plugin, delta) {
        if (plugin.draw !== undefined) {
            context.save();
            plugin.draw(context, delta);
            context.restore();
        }
    }
}
