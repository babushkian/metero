/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	(() => {
/******/ 		var scriptUrl;
/******/ 		if (__webpack_require__.g.importScripts) scriptUrl = __webpack_require__.g.location + "";
/******/ 		var document = __webpack_require__.g.document;
/******/ 		if (!scriptUrl && document) {
/******/ 			if (document.currentScript)
/******/ 				scriptUrl = document.currentScript.src;
/******/ 			if (!scriptUrl) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				if(scripts.length) {
/******/ 					var i = scripts.length - 1;
/******/ 					while (i > -1 && (!scriptUrl || !/^http(s?):/.test(scriptUrl))) scriptUrl = scripts[i--].src;
/******/ 				}
/******/ 			}
/******/ 		}
/******/ 		// When supporting browsers where an automatic publicPath is not supported you must specify an output.publicPath manually via configuration
/******/ 		// or pass an empty string ("") and set the __webpack_public_path__ variable from your code to use your own logic.
/******/ 		if (!scriptUrl) throw new Error("Automatic publicPath is not supported in this browser");
/******/ 		scriptUrl = scriptUrl.replace(/#.*$/, "").replace(/\?.*$/, "").replace(/\/[^\/]+$/, "/");
/******/ 		__webpack_require__.p = scriptUrl;
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};

;// CONCATENATED MODULE: ./img/expand_less.svg
/* harmony default export */ const expand_less = (__webpack_require__.p + "db993b821b0aa4bca99715960538f054.svg");
;// CONCATENATED MODULE: ./img/expand_more.svg
/* harmony default export */ const expand_more = (__webpack_require__.p + "730839144c126385607bf09f84d35c4f.svg");
;// CONCATENATED MODULE: ./js/Meter.js



class Meter {
    constructor(parent, item, rownumber) {
        this.parent = parent;
        this.item = item;
        this.record = document.createElement("div");
        this.record.className = "row";
        this.record.dataset.rowId = item.id;
        this.record.dataset.rowbumber = rownumber;

        this.inputString = document.createElement("input");
        this.inputString.className = "input_meter";
        this.inputString.id = `input-meter-${this.record.dataset.rowbumber}`;
        this.record.appendChild(this.inputString);
        const cle = document.createElement("div");
        cle.className = "controls";
        const ude = document.createElement("div");
        ude.className = "updown";
        this.up = document.createElement("button");
        this.up.className = "adjust";
        const upim = document.createElement("img");
        upim.src = expand_less;
        this.up.appendChild(upim);
        this.down = document.createElement("button");
        this.down.className = "adjust";
        const dowim = document.createElement("img");
        dowim.src = expand_more;
        this.down.appendChild(dowim);
        upim.className = "arrow";
        dowim.className = "arrow";

        ude.appendChild(this.up);
        ude.appendChild(this.down);
        cle.appendChild(ude);
        this.delb = document.createElement("button");
        this.delb.className = "delete";
        this.delb.innerText = "удалить";
        cle.appendChild(this.delb);
        this.record.appendChild(cle);

        this.inputString.value = this.item.name;
        // this.inputString.setAttribute("readonly", true);

        this.applyListeners();
    }

    applyListeners() {
        this.delButtonFunc = this.delRec.bind(this);
        this.delb.addEventListener("click", this.delButtonFunc);

        this.moveUp = this.move.bind(this, this.record.dataset.rowbumber, -1);
        this.up.addEventListener("click", this.moveUp);

        this.moveDown = this.move.bind(this, this.record.dataset.rowbumber, 1);
        this.down.addEventListener("click", this.moveDown);
        this.recEd = this.editRecord.bind(this);
        this.inputString.addEventListener("blur", this.recEd);
    }

    removeListeners() {
        this.delb.removeEventListener("click", this.delButtonFunc);
        this.up.removeEventListener("click", this.moveUp);
        this.down.removeEventListener("click", this.moveDown);
        this.inputString.removeEventListener("blur", this.recEd);
    }

    async delRec() {
        console.log("всё ", this);
        if (
            confirm("Вы уверены? все показания этого счетчика будут удалены!")
        ) {
            console.log("почему? ", this.item);
            const jsn = JSON.stringify({
                id: this.item.id,
            });
            console.log(jsn);
            URL = `${window.location.origin}/api/del_rec/`;
            //URL = "http://127.0.0.1:5000/api/del_rec/"
            await fetch(URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: jsn,
            });
            this.parent.draw();
        }
    }

    async move(ind, direction) {
        const index = Number(ind);
        const next = index + Number(direction);
        if (next >= 0 || next < this.parent.data.lenght) {
            URL = `${window.location.origin}/api/swap/`;
            //URL = "http://127.0.0.1:5000/api/swap/"
            await fetch(URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    from: this.parent.data[index].id,
                    to: this.parent.data[next].id,
                }),
            });
            this.parent.draw();
        }
    }

    async editRecord() {
        const tempValue = this.inputString.value;
        if (tempValue === this.item.name) {
            return;
        }

        if (tempValue === "") {
            alert("Пустое поле недопустимо!");
            this.inputString.value = this.item.name;
            return;
        }
        let uniqueFlag = true;
        this.parent.data.forEach((item, index) => {
            if (
                item.name === tempValue &&
                this.record.dataset.rowbumber != index
            ) {
                uniqueFlag = false;
            }
        });
        if (!uniqueFlag) {
            alert("Поля с повторяющимися названиями недопустимы!");
            this.inputString.value = this.item.name;
            return;
        }
        URL = `${window.location.origin}/api/nameedit/`;
        //URL = "http://127.0.0.1:5000/api/nameedit/"
        await fetch(URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id: this.item.id,
                name: tempValue,
            }),
        });
        this.parent.draw();
    }
}

;// CONCATENATED MODULE: ./js/MeterList.js


class MeterList {
    static recId = 0;
    constructor(parent, meterList) {
        console.log(window.location.href);
        this.parent = parent;
        this.meterList = meterList;
        this.recs = [];
        this.draw();
    }
    clear() {
        this.meterList.innerHTML = "";
        this.recs.forEach((item) => {
            item.removeListeners();
        });
    }

    removeRecordsListeners() {
        this.recs.forEach((item) => {
            item.removeListeners();
        });
    }

    async draw() {
        this.data = await this.getRecords();
        this.clear();
        this.data.sort((a, b) => a.order - b.order);
        this.data.forEach((item, index) => {
            this.showRecord(item, index);
        });
    }

    showRecord(item, index) {
        const m = new Meter(this, item, index);
        this.meterList.appendChild(m.record);
        this.recs.push(m);
    }

    async getRecords() {
        URL = `${window.location.origin}/api/get_meters/`;
        console.log(URL)

        //URL = `http://127.0.0.1:5000/api/${this.parent.usrId}/`;
        const meters = await fetch(URL);
        return await meters.json();
    }
}

;// CONCATENATED MODULE: ./js/NewRecord.js


class NewRecord {
    constructor(parentNode, listNode) {
        this.parentNode = parentNode;
        this.usrId = this.parentNode.dataset.userId;
        this.createForm();
        this.list = new MeterList(this, listNode);
    }

    createForm() {
        this.record = document.createElement("div");
        this.record.className = "row";
        this.record.classList.add("input");
        this.inputString = document.createElement("input");
        this.inputString.type = "text";
        this.inputString.className = "input_meter";
        this.inputString.placeholder = "Ведите название счетчика";
        this.inputString.id = "add_new_meter";
        this.inputString.name = "add_new_meter";
        const controls = document.createElement("div");
        controls.className = "controls";
        this.addButton = document.createElement("button");
        this.addButton.className = "add";
        this.addButton.innerText = "добавить";
        controls.appendChild(this.addButton);
        this.record.appendChild(this.inputString);
        this.record.appendChild(controls);
        this.parentNode.appendChild(this.record);
        this.addListeners();
    }

    addListeners() {
        const anr = this.addNewRecord.bind(this);
        this.addButton.addEventListener("click", anr);

        this.record.addEventListener("keyup", (e) => {
            if (e.key === "Enter") {
                anr();
            }
        });
    }

    async addNewRecord() {
        const meterName = this.inputString.value;
        if (meterName === "") {
            this.redBlink();
            return;
        }
        for (let i = 0; i < this.list.data.length; i++) {
            if (meterName === this.list.data[i].name) {
                alert("Поля с повторяющимися названиями недопустимы!");
                return;
            }
        }

        URL = `${window.location.origin}/api/add_rec/`;
	//URL = "http://127.0.0.1:5000/api/add_rec/"
        await fetch(URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user_id: this.usrId,
                name: meterName,
            }),
        });
        this.inputString.value = "";
        this.list.draw();
    }

    redBlink() {
        this.inputString.classList.add("blanc-error");

        const inter = setInterval(
            () => this.inputString.classList.toggle("blanc-error"),
            60
        );
        setTimeout(() => clearInterval(inter), 180);
    }
}

;// CONCATENATED MODULE: ./index.js

// import "./styles/style.css";


const addDiv = document.querySelector(".add_block");
const meterList = document.querySelector(".meter_block");

const nr = new NewRecord(addDiv, meterList);

/******/ })()
;