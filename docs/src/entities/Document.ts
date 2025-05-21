import { Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, UpdateDateColumn, DeleteDateColumn, AfterLoad } from "typeorm"
import { SerializedEditorState } from "lexical";

@Entity('documents')
export class Document {
    @PrimaryGeneratedColumn('uuid')
    id: string;

    @Column()
    user_id: string;

    @Column()
    title: string;

    @Column('jsonb', { nullable: true })
    state: SerializedEditorState;

    @Column('jsonb', { nullable: true })
    extra: Record<string, any>;

    @CreateDateColumn({ type: 'timestamp' })
    created_at: number;

    @UpdateDateColumn({ type: 'timestamp' })
    updated_at: number;

    @DeleteDateColumn({ type: 'timestamp', nullable: true })
    deleted_at: number | null;

    @AfterLoad()
    convertDatesToTimestamps() {
        this.updated_at = Math.floor(new Date(this.updated_at).getTime() / 1000);
        this.created_at = Math.floor(new Date(this.created_at).getTime() / 1000);
        this.deleted_at = this.deleted_at ? Math.floor(new Date(this.deleted_at).getTime() / 1000) : null;
    }
}
