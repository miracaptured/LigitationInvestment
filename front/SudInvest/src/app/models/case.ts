export class Case {
    name: string = "";
    status: string = "";
    claim: number = 0;
    description: string = "";

    constructor(name: string, status: string, claim: number, description: string) {
        this.name = name;
        this.status = status;
        this.claim = claim;
        this.description = description;
    }
}