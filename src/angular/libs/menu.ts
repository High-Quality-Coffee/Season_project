import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class Menu {
    // all category
    public data = {
        first: [],
        second: [],
        third: [],
    };
    // selected category
    public current = {
        first: null,
        second: null,
        third: null,
    };
    public redirect = null;

    public change(id = null) {
        if (!id) {
            this.current = {
                first: null,
                second: null,
                third: null,
            };
            return;
        }
        const handler = item => item.id === id;
        let res = this.data.first.find(handler);
        if (res !== undefined) {
            this.current.first = res;
            this.current.second = null;
            this.current.third = null;
            return;
        }
        res = this.data.second.find(handler);
        if (res !== undefined) {
            this.current.second = res;
            this.current.third = null;
            return;
        }
        res = this.data.third.find(handler);
        if (res !== undefined) {
            this.current.third = res;
            return;
        }
        if (!res) throw new Error("잘못된 메뉴");
    }
}

export default Menu;
