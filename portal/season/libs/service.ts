import { Injectable } from '@angular/core';
import Crypto from './crypto';
import Auth from './auth';
import File from './file';
import Alert from './alert';
import Loading from './loading';

@Injectable({ providedIn: 'root' })
export class Service {
    public auth: Auth;
    public file: File;
    public alert: Alert;
    public loading: Loading;
    public app: any;

    constructor() { }

    public async init(app: any) {
        if (app) {
            this.app = app;
            this.crypto = new Crypto();
            this.auth = new Auth(this);
            this.file = new File(this);
            this.alert = new Alert(this);
            this.loading = new Loading(this);
            await this.auth.init();
        }

        await this.loading.show();
        await this.auth.check();
        return this;
    }

    public async render(time: number = 0) {
        let timeout = () => new Promise((resolve) => {
            setTimeout(resolve, time);
        });
        if (time > 0) {
            this.app.ref.detectChanges();
            await timeout();
        }
        this.app.ref.detectChanges();
    }

    public href(url: any) {
        this.app.router.navigate(url);
    }

    public random(stringLength: number = 16) {
        const fchars = 'abcdefghiklmnopqrstuvwxyz';
        const chars = '0123456789abcdefghiklmnopqrstuvwxyz';
        let randomstring = '';
        for (let i = 0; i < stringLength; i++) {
            let rnum = null;
            if (i === 0) {
                rnum = Math.floor(Math.random() * fchars.length);
                randomstring += fchars.substring(rnum, rnum + 1);
            } else {
                rnum = Math.floor(Math.random() * chars.length);
                randomstring += chars.substring(rnum, rnum + 1);
            }
        }
        return randomstring;
    }
}

export default Service;