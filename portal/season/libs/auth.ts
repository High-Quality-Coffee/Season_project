import Service from './service';
import Request from './request';

export default class Auth {
    public verified: string | null = null;

    public timestamp: number = 0;
    public status: any = null;
    public loading: any = null;

    public session: any = {
        id: null,
        mail: null,
        role: null
    };

    constructor(public service: Service) {
        this.request = new Request();
    }

    public async init() {
        let { code, data } = await this.request.post('/auth/check');
        let { status, session } = data;

        this.verified = session.verified?session.verified:[];
        // this.verified = session.verified;

        if (code != 200)
            return this;

        this.timestamp = new Date().getTime();
        this.session = session;
        this.status = status;
        this.loading = true;
        return this;
    }

    public async check() {
        while (this.loading === null) {
            await this.service.render(100);
        }

        let diff = new Date().getTime() - this.timestamp;
        if (diff > 1000 * 60) {
            this.loading = null;
            await this.init();
        }
    }

    public async allow(roles: any = null, redirect: string | null = null) {
        if (roles === null) {
            if (this.service.loading.isshow)
                this.service.loading.hide();
            return true;
        }

        if (typeof roles == 'boolean') {
            if (roles === this.status) {
                if (this.service.loading.isshow)
                    this.service.loading.hide();
                return true;
            }
        } else {
            if (typeof roles == 'string')
                roles = [roles];

            if (roles.indexOf(this.session.role) >= 0) {
                if (this.service.loading.isshow)
                    this.service.loading.hide();
                return true;
            }
        }

        if (redirect) {
            location.href = redirect;
        }
        return false;
    }

    public show(roles: any = null, redirect: string | null = null) {
        if (roles === null) {
            return true;
        }

        if (typeof roles == 'boolean') {
            if (roles === this.status) {
                return true;
            }
        } else {
            if (typeof roles == 'string')
                roles = [roles];

            if (roles.indexOf(this.session.role) >= 0) {
                return true;
            }
        }

        if (redirect) {
            location.href = redirect;
        }
        return false;
    }

    public hash(password: string = '') {
        return this.service.crypto.SHA256(password).toString();
    }
}