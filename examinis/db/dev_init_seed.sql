-- Seed for development.

-- Clear
TRUNCATE TABLE public.user, public.role, public.user_status, public.difficulty, public.subject, public.option,
public.correct_option, public.question CASCADE;

-- Insert Difficulty
ALTER SEQUENCE difficulty_id_seq RESTART with 1;
INSERT INTO public.difficulty (name) VALUES
('Easy'), ('Medium'), ('Hard');

-- Insert Subject
ALTER SEQUENCE subject_id_seq RESTART with 1;
INSERT INTO public.subject (name) VALUES
('Mathematics'), ('Physics'), ('Chemistry'), ('Biology');

-- Insert Role
ALTER SEQUENCE role_id_seq RESTART with 1;
INSERT INTO public.role (name) VALUES
('Admin'), ('Professor'), ('Student');

-- Insert User Status
ALTER SEQUENCE user_status_id_seq RESTART with 1;
INSERT INTO public.user_status (name) VALUES
('Active'), ('Pending'), ('Inactive');

-- Insert User
ALTER SEQUENCE user_id_seq RESTART with 1;
INSERT INTO public.user (email, password, first_name, last_name, role_id, status_id, created_at, updated_at) VALUES
('admin@email.com', 'secret', 'Admin', 'L_Admin', 1, 1, NOW(), NOW()),
('professor@email.com', 'secret', 'Professor', 'L_Professor', 2, 1, NOW(), NOW()),
('student@email.com', 'secret', 'Student', 'L_Student', 3, 1, NOW(), NOW());
