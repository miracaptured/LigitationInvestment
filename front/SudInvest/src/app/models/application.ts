export class Application {
    application_id: number = 0;
    initiator_id: number = 0;
    name: string = "";
    status: string = "";
    claim: number = 0;
    description: string = "";
    initiator_role: string = "";

    constructor(
        application_id: number,
        initiator_id: number,
        name: string,
        status: string,
        claim: number,
        initiator_role: string,
        description: string)
    {
        this.application_id = application_id;
        this.initiator_id = initiator_id;
        this.name = name;
        this.status = status;
        this.claim = claim;
        this.initiator_role = initiator_role;
        this.description = description;
    }
}