export interface Tank {
    action_points: number;
    health_points: number;
    x: number;
    y: number;
    range: number;
}

export interface Player {
    id: number;
    name: string;
    tank: Tank;
    discord_id: number;
    avatar_url: string;
    is_dead: boolean;
    ad_vote?: any;
    game_set: number[];
    player_color: string;
}

export interface Game {
    id: number;
    guild_id: number;
    players: Player[];
    allowed_joining: boolean;
    max_players: number;
    game_talk_channel: number;
    commands_channel: number;
    logs_channel: number;
    grid_size_x: number;
    grid_size_y: number;
    is_action_day_1d: boolean;
    ad_duration: number;
    is_started: boolean;
    is_ended: boolean;
    next_ad_end: Date;
    game_start_date: Date;
}

export interface MoveEvent {
    direction: {
        x: number,
        y: number
    },

    position: {
        x: number,
        y: number
    },
    newActionPoints: number
}