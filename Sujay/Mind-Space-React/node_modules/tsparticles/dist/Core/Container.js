"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Container = void 0;
const Canvas_1 = require("./Canvas");
const Particles_1 = require("./Particles");
const Retina_1 = require("./Retina");
const FrameManager_1 = require("./FrameManager");
const Options_1 = require("../Options/Classes/Options");
const Utils_1 = require("../Utils");
class Container {
    constructor(id, sourceOptions, ...presets) {
        this.id = id;
        this.sourceOptions = sourceOptions;
        this.firstStart = true;
        this.started = false;
        this.destroyed = false;
        this.paused = true;
        this.lastFrameTime = 0;
        this.pageHidden = false;
        this.retina = new Retina_1.Retina(this);
        this.canvas = new Canvas_1.Canvas(this);
        this.particles = new Particles_1.Particles(this);
        this.drawer = new FrameManager_1.FrameManager(this);
        this.noise = {
            generate: () => {
                return {
                    angle: Math.random() * Math.PI * 2,
                    length: Math.random(),
                };
            },
            init: () => {
            },
            update: () => {
            },
        };
        this.interactivity = {
            mouse: {
                clicking: false,
                inside: false,
            },
        };
        this.bubble = {};
        this.repulse = { particles: [] };
        this.attract = { particles: [] };
        this.plugins = new Map();
        this.drawers = new Map();
        this.density = 1;
        this.options = new Options_1.Options();
        for (const preset of presets) {
            this.options.load(Utils_1.Plugins.getPreset(preset));
        }
        const shapes = Utils_1.Plugins.getSupportedShapes();
        for (const type of shapes) {
            const drawer = Utils_1.Plugins.getShapeDrawer(type);
            if (drawer) {
                this.drawers.set(type, drawer);
            }
        }
        if (this.sourceOptions) {
            this.options.load(this.sourceOptions);
        }
        this.fpsLimit = this.options.fpsLimit > 0 ? this.options.fpsLimit : 60;
        this.options.setTheme(undefined);
        this.eventListeners = new Utils_1.EventListeners(this);
        if (typeof IntersectionObserver !== "undefined" && IntersectionObserver) {
            this.intersectionObserver = new IntersectionObserver((entries) => this.intersectionManager(entries));
        }
    }
    play(force) {
        const needsUpdate = this.paused || force;
        if (this.firstStart && !this.options.autoPlay) {
            this.firstStart = false;
            return;
        }
        if (this.paused) {
            this.paused = false;
        }
        if (needsUpdate) {
            for (const [, plugin] of this.plugins) {
                if (plugin.play) {
                    plugin.play();
                }
            }
            this.lastFrameTime = performance.now();
        }
        this.draw();
    }
    pause() {
        if (this.drawAnimationFrame !== undefined) {
            Utils_1.Utils.cancelAnimation(this.drawAnimationFrame);
            delete this.drawAnimationFrame;
        }
        if (this.paused) {
            return;
        }
        for (const [, plugin] of this.plugins) {
            if (plugin.pause) {
                plugin.pause();
            }
        }
        if (!this.pageHidden) {
            this.paused = true;
        }
    }
    draw() {
        this.drawAnimationFrame = Utils_1.Utils.animate((timestamp) => this.drawer.nextFrame(timestamp));
    }
    getAnimationStatus() {
        return !this.paused;
    }
    setNoise(noiseOrGenerator, init, update) {
        if (!noiseOrGenerator) {
            return;
        }
        if (typeof noiseOrGenerator === "function") {
            this.noise.generate = noiseOrGenerator;
            if (init) {
                this.noise.init = init;
            }
            if (update) {
                this.noise.update = update;
            }
        }
        else {
            if (noiseOrGenerator.generate) {
                this.noise.generate = noiseOrGenerator.generate;
            }
            if (noiseOrGenerator.init) {
                this.noise.init = noiseOrGenerator.init;
            }
            if (noiseOrGenerator.update) {
                this.noise.update = noiseOrGenerator.update;
            }
        }
    }
    destroy() {
        this.stop();
        this.canvas.destroy();
        for (const [, drawer] of this.drawers) {
            if (drawer.destroy) {
                drawer.destroy(this);
            }
        }
        for (const key of this.drawers.keys()) {
            this.drawers.delete(key);
        }
        this.destroyed = true;
    }
    exportImg(callback) {
        this.exportImage(callback);
    }
    exportImage(callback, type, quality) {
        var _a;
        return (_a = this.canvas.element) === null || _a === void 0 ? void 0 : _a.toBlob(callback, type !== null && type !== void 0 ? type : "image/png", quality);
    }
    exportConfiguration() {
        return JSON.stringify(this.options, undefined, 2);
    }
    refresh() {
        return __awaiter(this, void 0, void 0, function* () {
            this.stop();
            yield this.start();
        });
    }
    stop() {
        if (!this.started) {
            return;
        }
        this.firstStart = true;
        this.started = false;
        this.eventListeners.removeListeners();
        this.pause();
        this.particles.clear();
        this.canvas.clear();
        if (this.interactivity.element instanceof HTMLElement && this.intersectionObserver) {
            this.intersectionObserver.observe(this.interactivity.element);
        }
        for (const [, plugin] of this.plugins) {
            if (plugin.stop) {
                plugin.stop();
            }
        }
        for (const key of this.plugins.keys()) {
            this.plugins.delete(key);
        }
        this.particles.linksColors = new Map();
        delete this.particles.grabLineColor;
        delete this.particles.linksColor;
    }
    loadTheme(name) {
        return __awaiter(this, void 0, void 0, function* () {
            this.options.setTheme(name);
            yield this.refresh();
        });
    }
    start() {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.started) {
                return;
            }
            yield this.init();
            this.started = true;
            this.eventListeners.addListeners();
            if (this.interactivity.element instanceof HTMLElement && this.intersectionObserver) {
                this.intersectionObserver.observe(this.interactivity.element);
            }
            for (const [, plugin] of this.plugins) {
                if (plugin.startAsync !== undefined) {
                    yield plugin.startAsync();
                }
                else if (plugin.start !== undefined) {
                    plugin.start();
                }
            }
            this.play();
        });
    }
    init() {
        return __awaiter(this, void 0, void 0, function* () {
            this.retina.init();
            this.canvas.init();
            this.fpsLimit = this.options.fpsLimit > 0 ? this.options.fpsLimit : 60;
            const availablePlugins = Utils_1.Plugins.getAvailablePlugins(this);
            for (const [id, plugin] of availablePlugins) {
                this.plugins.set(id, plugin);
            }
            for (const [, drawer] of this.drawers) {
                if (drawer.init) {
                    yield drawer.init(this);
                }
            }
            for (const [, plugin] of this.plugins) {
                if (plugin.init) {
                    plugin.init(this.options);
                }
                else if (plugin.initAsync !== undefined) {
                    yield plugin.initAsync(this.options);
                }
            }
            this.canvas.initSize();
            this.particles.init();
            this.particles.setDensity();
        });
    }
    intersectionManager(entries) {
        if (!this.options.pauseOnOutsideViewport) {
            return;
        }
        for (const entry of entries) {
            if (entry.target !== this.interactivity.element) {
                continue;
            }
            if (entry.isIntersecting) {
                this.play();
            }
            else {
                this.pause();
            }
        }
    }
}
exports.Container = Container;
